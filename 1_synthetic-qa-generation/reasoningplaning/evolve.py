import heapq
import math
import random
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import itertools

import logging
# logger = None
def setup_logging(seed_data: str):
    log_filename = f"{seed_data.replace('.jsonl', '').replace('.json', '')}.log"
    if not os.path.exists(log_filename):
        os.mknod(log_filename)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler(log_filename), logging.StreamHandler()],
    )
    return logging.getLogger(__name__)


import sys
import ast
import json
import uuid
from typing import List, Tuple, Dict, Any, Optional

import pandas as pd
import numpy as np
from enum import Enum

import time
import torch
from datasets import Dataset, DatasetDict
from transformers import pipeline
from transformers.pipelines.pt_utils import KeyDataset
from tqdm.auto import tqdm

import markdown
from bs4 import BeautifulSoup
from datasets import load_dataset
import os, openai
from dotenv import load_dotenv
from openai import AzureOpenAI, RateLimitError

load_dotenv()  # take environment variables from .env.

NUM_TRY_BEFORE_SEARCH = 16

def separateSteps(steps: List[str], mode: str = 'join') -> Any:
    delimiter = "\n\n"
    if mode == 'join':
        if not isinstance(steps, list):
            raise TypeError("For 'join' mode, 'steps' must be a list of strings.")
        return delimiter.join(steps)
    elif mode == 'split':
        if not isinstance(steps, str):
            raise TypeError("For 'split' mode, 'steps' must be a string.")
        return steps.split(delimiter)
    else:
        raise ValueError("Mode should be either 'join' or 'split'.")

# Helper function to check correctness of a generated response
def checkCorrectness(generated_response: str, expected_answer: str) -> bool:
    sentences = re.split(
        r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', generated_response.strip()
    )
    last_sentence = sentences[-1] if sentences else ''
    return expected_answer.strip() in last_sentence.strip()


class BranchMaker:
    def __init__(self, azureAiService):
        self.azureAiService = azureAiService
        self.default_prompt = (
            "Please complete the answer for the question based on the given steps without generating existing steps again, "
            "and separate your following steps using \\n\\n.\n\n"
        )
        # self.azureAiService.startService()

    def generateBranch(self, node_prefix: str, num_copies) -> List[str]:
        """
        Combine the default prompt with the node prefix and generate a response.

        Parameters:
        - node_prefix (str): The current solution prefix.

        Returns:
        - str: Generated response from LLM.
        """
        prompt = self.default_prompt + node_prefix
        batch_response = self.azureAiService.generateResponse(prompt, num_copies)
        return batch_response # Assuming the response format has ['role'] entries and 'assistant' response

    def evaluateCorrectness(self, response: str, expected_answer: str) -> bool:
        return checkCorrectness(response, expected_answer)


# Define the node class
class Nde:
    def __init__(self, solution_prefix: str, parent: Optional['Nde'] = None):
        self.solution_prefix = solution_prefix  # Solution prefix as a single string
        self.parent = parent  # Reference to the parent node
        self.numVisited = 0  # Visit count (number of times selected)
        self.numOfTtlBranches = 0  # Total number of branches generated from this node
        self.trueBranches = 0  # Number of correct branches
        self.reward: Optional[float] = None  # Monte Carlo estimation (c/k)
        self.branchesQ: Dict[str, float] = {}  # Q(s, r): estimated value for each branch
        self.branches: List[str] = []  # Set of all branches from this node
        self.falseBranches: List[str] = []  # List of incorrect branches
        self.children: List['Nde'] = []  # List of child states

    def addBranch(self, branch: str):
        self.branches.append(branch)

    def addFalseBranch(self, branch: str):
        if branch not in self.falseBranches:
            self.falseBranches.append(branch)

    def get_full_solution(self) -> str:
        # Return the complete solution from the root to this node
        if self.parent:
            return self.parent.get_full_solution() + '\n\n' + self.solution_prefix
        else:
            return self.solution_prefix

    def getNewTxt(self) -> str:
        """
        Return the new text added at this node compared to the parent.
        """
        if self.parent:
            parent_text = self.parent.solution_prefix
            new_text = self.solution_prefix[len(parent_text):].strip()
            return new_text
        else:
            # Root node (the question)
            return self.solution_prefix.strip()

    def getTxtWithLabels(self) -> Dict[str, Any]:
        """
        Return a nested dictionary where each node contains:
        - 'text': The new text at this node.
        - 'mc_value': The reward value at this node.
        - 'children': A list of child nodes with the same structure.
        """
        data = {
            'text': self.getNewTxt(),
            'mc_value': self.reward,
            'children': [child.getTxtWithLabels() for child in self.children]
        }
        return data


# Define the Search Tree class
class SearchTree:
    def __init__(self):
        self.root: Optional[Nde] = None
        self.nodes: List[Nde] = []  # List of all states

    def addNode(self, node: Nde):
        self.nodes.append(node)

# Define the Candidate Pool as a priority queue with update capability
class CandidatePool:
    def __init__(self):
        self.heap: List[Tuple[float, int]] = []  # Heap of (-priority, unique_id)
        self.entry_finder: Dict[int, Tuple[float, int]] = {}  # Maps unique_id to (-priority, unique_id)
        self.counter = itertools.count()  # Unique sequence count
        self.id_to_branch: Dict[int, Tuple[Nde, str]] = {}  # Maps unique_id to (node, branch)
        self.latest_id_per_branch: Dict[Tuple[int, str], int] = {}  # Maps (node_id, branch) to unique_id

    def addOrUpdate(self, node: Nde, branch: str, priority: float):
        """
        Add a new branch or update the priority of an existing branch.

        Parameters:
        - node (Nde): The node associated with the branch.
        - branch (str): The branch string.
        - priority (float): The new priority score.
        """
        node_id = id(node)  # Unique identifier for the node object
        branch_key = (node_id, branch)

        # Check if the branch already exists in the pool
        if branch_key in self.latest_id_per_branch:
            # Previous unique_id exists; it is now outdated
            old_unique_id = self.latest_id_per_branch[branch_key]
            # Mark the old entry as invalid by removing it from entry_finder
            if old_unique_id in self.entry_finder:
                del self.entry_finder[old_unique_id]
                del self.id_to_branch[old_unique_id]

        # Assign a new unique_id for the updated branch
        unique_id = next(self.counter)
        self.latest_id_per_branch[branch_key] = unique_id

        # Add the new entry to the heap and mappings
        heapq.heappush(self.heap, (-priority, unique_id))  # Max-heap using negative priority
        self.entry_finder[unique_id] = (-priority, unique_id)
        self.id_to_branch[unique_id] = (node, branch)

    def pop(self) -> Tuple[Optional[Nde], Optional[str]]:
        """
        Pop the branch with the highest priority.

        Returns:
        - Tuple[Optional[Nde], Optional[str]]: The node and branch string, or (None, None) if empty.
        """
        while self.heap:
            neg_priority, unique_id = heapq.heappop(self.heap)
            # Check if this unique_id is still valid
            if unique_id in self.entry_finder:
                # Valid entry
                node, branch = self.id_to_branch.pop(unique_id)
                del self.entry_finder[unique_id]
                # Remove from latest_id_per_branch
                node_id = id(node)
                branch_key = (node_id, branch)
                if self.latest_id_per_branch.get(branch_key) == unique_id:
                    del self.latest_id_per_branch[branch_key]
                return node, branch
            # Else, outdated entry; skip
        return None, None

    def is_empty(self) -> bool:
        return not self.entry_finder



MAX_ITERATIONS = 1
MAX_RETRIES = 2
GRND_TRUTH_COL = "final_answer"

def mdToText(md, do_md_to_text=True):
    if not do_md_to_text:
        return md
    assert md is not None, "Markdown is None"
    html = markdown.markdown(md)
    soup = BeautifulSoup(html, features='html.parser')
    return soup.get_text()


class Mutation(Enum):
    FRESH_START = 0
    ADD_CONSTRAINTS = 1
    DEEPEN = 2
    CONCRETIZE = 3
    INCREASE_REASONING = 4
    COMPLICATE = 5
    SWITCH_TOPIC = 6

# Retrieved from https://github.com/nlpxucan/WizardLM/tree/main
base_depth_instruction = "I want you act as a Prompt Rewriter.\r\n \
					Your objective is to rewrite a given prompt into a more complex version to make those famous AI systems (e.g., chatgpt and GPT4) a bit harder to handle.\r\n \
					But the rewritten prompt must be reasonable and must be understood and responded by humans.\r\n \
					Your rewriting cannot omit the non-text parts such as the table and code in #The Given Prompt#:. Also, please do not omit the input in #The Given Prompt#. \r\n \
					You SHOULD complicate the given prompt using the following method: \r\n\
					{} \r\n\
					You should try your best not to make the #Rewritten Prompt# become verbose, #Rewritten Prompt# can only add 10 to 20 words into #The Given Prompt#. \r\n\
					'#The Given Prompt#', '#Rewritten Prompt#', 'given prompt' and 'rewritten prompt' are not allowed to appear in #Rewritten Prompt#\r\n"

base_breadth_instruction = "I want you act as a Prompt Creator.\r\n\
Your goal is to draw inspiration from the #Given Prompt# to create a brand new prompt.\r\n\
This new prompt should belong to the same domain as the #Given Prompt# but be even more rare.\r\n\
The LENGTH and complexity of the #Created Prompt# should be similar to that of the #Given Prompt#.\r\n\
The #Created Prompt# must be reasonable and must be understood and responded by humans.\r\n\
'#Given Prompt#', '#Created Prompt#', 'given prompt' and 'created prompt' are not allowed to appear in #Created Prompt#\r\n"

complicate_prompt = base_depth_instruction.format("#Given Prompt# to make it slightly more complicated.'")
constraints_prompt = base_depth_instruction.format("Please add one more constraints/requirements into #The Given Prompt#'")
deepen_prompt = base_depth_instruction.format("If #The Given Prompt# contains inquiries about certain issues, the depth and breadth of the inquiry can be increased.")
concretizing_prompt = base_depth_instruction.format("Please replace general concepts with more specific concepts.")
reasoning_prompt = base_depth_instruction.format("If #The Given Prompt# can be solved with just a few simple thinking processes, you can rewrite it to explicitly request multiple-step reasoning.")

class WizardLM:
    def __init__(
            self,
            llm_pipeline: pipeline = None,
            seed_data: List[str] = None,
            column_names: List[str] = ["instruction"],
            num_rows: int = 10,
            min_len_chars: int = 512,
            max_len_chars: int = 1024,
            verbose: bool = False,
            language: str = "Chinese",
            expCnst=0.125,
            alpha=0.5,
            beta=0.9,
            maxSolutionLen=512,
            numBranches=4,
            maxSrch=4,
            maxBranches=40,
            saveAsTree=True,
    ):
        """
        Open-Source Implementation of https://arxiv.org/abs/2304.12244

        :param llm_pipeline: Pipeline that takes a HF dataset containing one string column and returns a list of strings
        :param seed_data: Optional data to create Q:A pairs from, list of strings containing prompts
        :param num_rows: Number of desired Q:A pairs
        :param min_len_bytes: Lower limit for prompt length in bytes
        :param max_len_bytes: Upper limit for prompt length in bytes
        :param verbose: Whether to enable verbose printing.
        """
        self.branchMaker = BranchMaker(llm_pipeline)
        self.expected_answer = None
        self.expCnst = expCnst
        self.alpha = alpha
        self.beta = beta
        self.maxSolutionLen = maxSolutionLen
        self.numBranches = numBranches
        self.maxSrch = maxSrch
        self.maxBranches = maxBranches
        self.saveAsTree = saveAsTree
        self.mct = SearchTree()
        self.candidatePool = CandidatePool()
        self.numSrched = 0
        self.numOfTtlBranches = 0

        self.maxIdx = -100
        self.llm_pipeline = llm_pipeline
        self.column_names = column_names
        self.num_rows = num_rows
        self.verbose = verbose
        self.seed_text_dict = dict()
        self.seed_data = seed_data
        self.prompts = dict()
        self.final_prompts = dict()
        self.final_answers = []
        self.min_len_bytes = min_len_chars
        self.max_len_bytes = max_len_chars
        self.prompt_templates = dict()
        self.prompt_templates['base'] = ""
        seed = None
        np.random.seed(seed)
        self.language = language
        self.prompt_templates[Mutation.FRESH_START] = \
            self.prompt_templates['base'] + \
f"""Write one question or request containing one or more of the following words. Write in {self.language}.: <PROMPT>"""

        self.prompt_templates[Mutation.COMPLICATE] = \
            self.prompt_templates['base'] + \
f"""{complicate_prompt}\nWrite in {self.language}.

#Given Prompt#:
<PROMPT>
"""

        self.prompt_templates[Mutation.ADD_CONSTRAINTS] = \
            self.prompt_templates['base'] + \
f"""{constraints_prompt}\nWrite in {self.language}.

#The Given Prompt#:
<PROMPT>
"""

        self.prompt_templates[Mutation.DEEPEN] = \
            self.prompt_templates['base'] + \
f"""{deepen_prompt}\nWrite in {self.language}.

#The Given Prompt#:
<PROMPT>
"""

        self.prompt_templates[Mutation.CONCRETIZE] = \
            self.prompt_templates['base'] + \
f"""{concretizing_prompt}\nWrite in {self.language}.

#The Given Prompt#:
<PROMPT>
"""

        self.prompt_templates[Mutation.INCREASE_REASONING] = \
            self.prompt_templates['base'] + \
f"""{reasoning_prompt}\nWrite in {self.language}.

#The Given Prompt#:
<PROMPT>
"""

        self.prompt_templates[Mutation.SWITCH_TOPIC] = \
            self.prompt_templates['base'] + \
f"""{base_breadth_instruction}\nWrite in {self.language}.

#Given Prompt#:
<PROMPT>
"""
    def run(self):
        self.createSeedPrompts()
        self.createPrompts()
        self.createAnswers()

        list_qa = []
        for i in range(len(self.final_prompts)):
            if len(self.final_answers[i]) > 10:
                list_qa.append(
                    {
                        'input': self.final_prompts[i],
                        'output': self.final_answers[i],
                    }
                )
        with open(f"{self.seed_data.replace('.jsonl', '').replace('json', '')}.%s.json" % str(uuid.uuid4())[:4], "wt") as f:
            f.write(json.dumps(list_qa, indent=2, ensure_ascii=False))        

    def monteCarloEstimation(self, node: Nde):
        numTrueBranches = 0  # Correct branches count
        falseBranches = []
        trueBranches = []
        genBranches = self.branchMaker.generateBranch(node.solution_prefix, self.numBranches)

        node.numVisited += 1

        for i, branch in enumerate(genBranches):
            if branch is None or not branch:
                continue
            self.numOfTtlBranches += 1

            # Generate branch r_i
            node.addBranch(branch)

            # Evaluate correctness of final answer in branch
            fullSolution = (node.solution_prefix + '\n\n' + branch).strip() if node.solution_prefix else branch
            isCorrect = self.branchMaker.evaluateCorrectness(fullSolution, self.expected_answer)

            if isCorrect:
                numTrueBranches += 1
                trueBranches.append(branch)
            else:
                falseBranches.append(branch)
                node.addFalseBranch(branch)  # Track incorrect branches

        # Update total branches and correct branches
        node.numOfTtlBranches += self.numBranches
        node.trueBranches += numTrueBranches
        node.reward = node.trueBranches / node.numOfTtlBranches if node.numOfTtlBranches > 0 else 0

        # logger.info(f"Monte Carlo Estimation for Nde ID {self.mct.nodes.index(node)}: reward = {node.reward:.2f}, Total Rollouts = {node.numOfTtlBranches}, Correct Rollouts = {node.trueBranches}\n")

        if node.reward == 1.0:
            # Add all correct branches to the tree as new states
            for branch in trueBranches:
                self.addTrueBranch2Tree(node, branch)
        elif node.reward == 0.0:
            # Nde is incorrect; no further action
            return
        else:
            # 0 < reward(s) < 1.0
            # Add correct branches to the tree
            for branch in trueBranches:
                self.addTrueBranch2Tree(node, branch)
            # Add incorrect branches to candidate pool with updated priorities
            for branch in falseBranches:
                priority = self.computeSelectionScore(node, branch)
                self.candidatePool.addOrUpdate(node, branch, priority)

    def computeHrdScor(self, node: Nde, branch: str) -> float:
        # Count words in the branch
        word_count = len(branch.split())
        length_penalty = word_count / self.maxSolutionLen
        hardness = (self.alpha ** (1 - node.reward)) * (self.beta ** length_penalty)
        return hardness

    def computeVistScor(self, node: Nde) -> float:
        N_total = sum(s.numVisited for s in self.mct.nodes)
        if N_total == 0:
            N_total = 1  # Prevent division by zero
        seldomvisit = self.expCnst * (math.sqrt(N_total)) / (1 + node.numVisited)
        return seldomvisit

    def computeSelectionScore(self, node: Nde, branch: str) -> float:
        hardness = self.computeHrdScor(node, branch)
        seldomvisit = self.computeVistScor(node)
        score = hardness + seldomvisit
        return score

    def selectionPhase(self) -> Tuple[Optional[Nde], Optional[str]]:
        selected_node, selected_branch = self.candidatePool.pop()
        return selected_node, selected_branch

    def addTrueBranch2Tree(self, parent_node: Nde, branch: str):
        new_solution_prefix = (parent_node.solution_prefix + '\n\n' + branch).strip() if parent_node.solution_prefix else branch
        new_node = Nde(solution_prefix=new_solution_prefix, parent=parent_node)
        new_node.reward = 1.0  # Since the branch is correct
        new_node.numOfTtlBranches = 0
        new_node.trueBranches = 0
        self.mct.addNode(new_node)
        parent_node.children.append(new_node)  # Add to parent's children


    def expansionPhaseBinSrch(self, parent_node: Nde, branch: str):
        """
        Parameters:
        - parent_node (Nde): The node from which the branch was selected.
        - branch (str): The branch string that was selected and is incorrect.
        """
        # Separate the branch into individual steps
        steps = separateSteps(branch, mode='split')

        # Perform binary search to find incorrect steps
        self.binSrchIncorrectStep(parent_node, steps, 0, len(steps) - 1)

    def binSrchIncorrectStep(self, s_ast: Nde, steps: List[str], left: int, right: int):
        """
        Recursively call bin search

        Parameters:
        - s_ast (Nde): The selected parent node.
        - steps (List[str]): The branch steps as a list.
        - left (int): Left index of the current search interval.
        - right (int): Right index of the current search interval.
        """
        if left > right:
            return

        mid = (left + right) // 2
        new_steps = steps[left:mid + 1]
        if new_steps:
            prefix_solution = s_ast.solution_prefix + '\n\n' + separateSteps(new_steps, mode='join')
        else:
            assert False
            prefix_solution = s_ast.solution_prefix
        # Create new node s_new
        s_new = Nde(solution_prefix=prefix_solution.strip(), parent=s_ast)
        self.mct.addNode(s_new)
        s_ast.children.append(s_new)

        # Perform Monte Carlo estimate
        self.monteCarloEstimation(s_new)

        if s_new.reward == 0:
            # Found incorrect step; continue searching in the left half to find earlier incorrect steps
            self.binSrchIncorrectStep(s_ast, steps, left, mid - 1)
        else:
            self.binSrchIncorrectStep(s_new, steps, mid + 1, right)

    def maintenancePhase(self, node: Nde):
        for branch in node.falseBranches:
            # Since we've already determined these branches are incorrect, no need to re-evaluate correctness
            priority = self.computeSelectionScore(node, branch)
            self.candidatePool.addOrUpdate(node, branch, priority)
            # logger.info(f"Updated Incorrect Rollout: '{branch}' with new priority: {priority:.4f}")

    def collectSolutionPrefixes(self) -> List[Dict[str, Any]]:
        collected_data = []
        for node in self.mct.nodes:
            solution_prefix = node.solution_prefix
            mc_value = node.reward
            collected_data.append({
                "solution_prefix": solution_prefix,
                "mc_value": mc_value
            })
        return collected_data

    def collectTreeStructure(self) -> Dict[str, Any]:
        if self.mct.root:
            tree_data = self.mct.root.getTxtWithLabels()
            return tree_data
        return {}


    def resetPrmState(self):
        self.expected_answer = None
        self.mct = SearchTree()  # Reset search tree
        self.candidatePool = CandidatePool()  # Reset candidate pool
        self.numSrched = 0
        self.numOfTtlBranches = 0
        self.collected_data = []  # Clear collected data

    def genPrm(self, question: str, answer: str) -> List:
        self.resetPrmState()

        logger.info(f"Running genPrm for question: '{question}'\n")
        # Initialization
        initial_node = Nde(solution_prefix=question, parent=None)
        self.expected_answer = answer
        self.mct.root = initial_node
        self.mct.addNode(initial_node)
        self.numSrched = 0

        # Monte Carlo Estimation for initial_node
        self.monteCarloEstimation(initial_node)

        # Main loop
        while self.numSrched < self.maxSrch and self.numOfTtlBranches < self.maxBranches and not self.candidatePool.is_empty():
            # Selection Phase
            selected_node, selected_branch = self.selectionPhase()
            if selected_node is None or selected_branch is None:
                # logger.info("No more candidates to explore. Terminating search.\n")
                break

            self.expansionPhaseBinSrch(selected_node, selected_branch)

            # Maintenance Phase
            self.maintenancePhase(selected_node)

            # Increment search count
            self.numSrched += 1

        if self.saveAsTree:
            data = self.collectTreeStructure()
        else:
            data = self.collectSolutionPrefixes()
        return data

    def shouldProcessQuestion(self, question: Dict[str, str]) -> bool:
        prompt = question[self.column_names]
        correct_answer = question[GRND_TRUTH_COL]

        has_correct = False
        has_incorrect = False

        initial_batch_answers = self.branchMaker.generateBranch(prompt, NUM_TRY_BEFORE_SEARCH)

        for answer in initial_batch_answers:
            if answer and self.branchMaker.evaluateCorrectness(answer, correct_answer):
                has_correct = True
            else:
                has_incorrect = True

            if has_correct and has_incorrect:
                logger.info(f"Question passed filter: {question['problem']}")
                return True

        return False
  
    def processQuestion(self, question: Dict[str, str]):
        # logger.info(f"Processing question with genPrm: {question[self.column_names]}")
        reasoning_steps = self.genPrm(question[self.column_names], question[GRND_TRUTH_COL])
        collected_data = {
            "question": question[self.column_names],
            GRND_TRUTH_COL: question[GRND_TRUTH_COL],
            "reasoning_steps": reasoning_steps,
        }
        return collected_data
  
    def saveQuestionData(self, collected_data: Dict, index: int, output_path: str):
        collected_data["question_id"] = index
        with open(output_path, "a") as fd:
            line = json.dumps(collected_data) #json.dumps(list_q, indent=2, ensure_ascii=False)
            fd.write(f"{line}\n")
        logger.debug(f"Question {index} is saved to {output_path}")

    def runQuestionOnly(self):
        self.createSeedPrompts()
        self.createPrompts()

        list_q = []
        for k in self.final_prompts:
            list_q.append(
                {
                    "idx": self.final_prompts[k]["idx"],
                    "preidx": self.final_prompts[k]["preidx"],
                    self.column_names: k,
                    GRND_TRUTH_COL: self.final_prompts[k][GRND_TRUTH_COL]
                    # 'input': self.final_prompts[k],
                }
            )
        del self.final_prompts
        output_file = f"{self.seed_data.replace('.jsonl', '').replace('.json', '')}.%s.json" % str(uuid.uuid4())[:4]
        processed_count = 0
        for question in list_q:
            if self.shouldProcessQuestion(question):
                collected_data = self.processQuestion(question)
                self.saveQuestionData(collected_data, question['idx'], output_file)
                processed_count += 1
            else:
                logger.info(f"Skipping question: {question[self.column_names]}")

        # Log summary
        logger.info(
            f"Total questions processed by genPrm: {processed_count}/{len(list_q)} inf file>> {output_file}"
        )

    def createSeedPrompts(self):
        """
        Turn self.seed_data into a list of strings of text self.source_text_list
        Each text string can represent as little as a word, or as much as document.
        Just has to be representative of some concept or body of text.

        :return: None
        """
        if isinstance(self.seed_data, str) and os.path.exists(self.seed_data):
            data = load_dataset("json", data_files=self.seed_data)
            self.seed_text_dict = dict()
            for d in data['train']:
                s = ""
                if isinstance(self.column_names, str):
                    s = d[self.column_names]
                else:
                    assert False, "column_names must be a str"
                    for col in self.column_names:
                        s += d[col] + "\n"
                # self.seed_text_dict.append(s.strip())
                self.seed_text_dict[s.strip()] = {
                        "idx": d["idx"],
                        GRND_TRUTH_COL: d[GRND_TRUTH_COL]
                    }
                if int(d["idx"]) > self.maxIdx:
                    self.maxIdx = int(d["idx"])
            assert self.seed_text_dict, "data import failed, got empty list"
            self.maxIdx = self.maxIdx + 10

    def createPrompts(self):
        logger.info("Creating %d prompts." % self.num_rows)
        assert self.seed_text_dict, "must have seed text list"
        t0 = time.time()
        self.prompts.clear()
        
        # for i in range(self.num_rows):
        #     new_prompt = np.random.choice(self.seed_text_dict)
        #     self.prompts.append(new_prompt)
        #@#FORTST comment above and replaced by below
        self.num_rows = len(self.seed_text_dict)
        for new_prompt in self.seed_text_dict:
            # self.prompts.append(new_prompt)
            self.prompts[new_prompt] = {
                        "idx": self.seed_text_dict[new_prompt]["idx"],
                        GRND_TRUTH_COL: self.seed_text_dict[new_prompt][GRND_TRUTH_COL]
                    }
        
        i = 0
        logger.info(f"length of self prompts={len(self.prompts)}")

        while self.mutate(i):
            logger.info("Iteration: %d" % i)
            i += 1
            if i >= MAX_ITERATIONS:
                logger.info("Reached maximum number of iterations.")
                break            
        t1 = time.time()
        logger.info("Done creating %d prompts in %.4f seconds." % (len(self.final_prompts), t1 - t0))
        #@# include the original prompt into final_prompts
        for k in self.seed_text_dict:
            self.final_prompts[k] = {
                    "idx": self.seed_text_dict[k]["idx"],
                    "preidx": int(-100),
                    "preproblem": "",
                    GRND_TRUTH_COL: self.seed_text_dict[k][GRND_TRUTH_COL]
                }

    def createAnswers(self):
        logger.info("Creating answers for %d prompts." % len(self.final_prompts))
        t0 = time.time()
        ds = self.convertListToDataset(self.final_prompts)
        self.final_answers = self.llm_pipeline(ds['train'])
        t1 = time.time()
        logger.info("Done creating answers for %d prompts in %.4f seconds." % (ds['train'].num_rows, t1 - t0))

    def convertListToDataset(self, text_list):
        df = pd.DataFrame({'text': text_list})
        ds = DatasetDict()
        ds['train'] = Dataset.from_pandas(df)
        return ds

    def mutate(self, iteration):
        assert len(self.prompts) == self.num_rows or len(self.prompts) == len(self.seed_text_dict)
        list_prompts = []
        mutations = []
        original_prompts = []
        # for i in range(self.num_rows):
        for k in self.prompts:
            mutation = np.random.choice(Mutation)
            mutations.append(mutation)
            # if mutation == Mutation.FRESH_START:
            #     mutation = Mutation.COMPLICATE
            before = k #self.prompts[i]
            prompt = self.prompt_templates[mutation].replace("<PROMPT>", before)
            
            if mutation == Mutation.SWITCH_TOPIC:
                prompt += "#Created Prompt#:\r\n"
            else:
                prompt += "#Rewritten Prompt:\r\n"
            
            logger.info(f"Full prompt={prompt}")
            list_prompts.append(prompt)
            original_prompts.append(k)

        ds = self.convertListToDataset(list_prompts)
        assert ds['train'].num_rows == len(list_prompts) == self.num_rows == len(self.prompts)
        
        # Processing transformed prompts using the LLM pipeline
        t0 = time.time()
        after = self.llm_pipeline(ds['train'])
        assert len(after) == self.num_rows
        t1 = time.time()
        
        llm_pipeline_name = self.llm_pipeline.__class__.__name__
        logger.info(f"{llm_pipeline_name} took {t1 - t0:.4f} seconds")

        for i in range(len(after)):
            after[i] = after[i].split("Prompt#:")[-1].strip()
            for pp in ['New Prompt:\n', 'New Prompt: ']:
                if after[i][:len(pp)] == pp:
                    after[i] = after[i][len(pp):]
            after[i] = after[i].strip()
            
            #use_new_prompt, why = self.changeApproved(self.prompts[i], after[i])
            use_new_prompt = True

            original_p = original_prompts[i]
            if self.verbose:
                logger.info("===========================")
                logger.info("Old Prompt: %s" % original_p)
                logger.info("Mutation: %s" % mutations[i].name)
                logger.info("New Prompt: %s" % after[i])
                logger.info("===========================")

            if use_new_prompt:
                original_itm = self.prompts[original_p]
                self.maxIdx = self.maxIdx + 1
                self.final_prompts[after[i]] = {
                    "idx": self.maxIdx,
                    "preidx": original_itm["idx"],
                    "preproblem": original_p,
                    GRND_TRUTH_COL: original_itm[GRND_TRUTH_COL]
                }
                del self.prompts[original_p]
                chosen_prmp = np.random.choice(list(self.seed_text_dict.keys()))
                self.prompts[chosen_prmp] = {
                        "idx": self.seed_text_dict[chosen_prmp]["idx"],
                        GRND_TRUTH_COL: self.seed_text_dict[chosen_prmp][GRND_TRUTH_COL]
                    }
                # if self.max_len_bytes >= len(after[i]) >= self.min_len_bytes:
                #     self.final_prompts.append(after[i])
                #     logger.info("Prompt was accepted, now have %d good prompts." % len(self.final_prompts))
                #     self.prompts[i] = np.random.choice(self.seed_text_dict)
                #     logger.info("Creating new prompt.")
                # else:
                #     self.prompts[i] = after[i]
                #     logger.info("Prompt was successfully modified.")
            else:
                logger.info("Mutation rejected, will try again. Reason: %s" % why)
            # logger.info("", flush=True)
        logger.info("final_prompt=")
        logger.info(self.final_prompts)
        return len(self.final_prompts) <= self.num_rows

    def changeApproved(self, before, after):
        if before == after:
            return False, "same"
        if after.count('\n') > after.count(" ") * 2:
            return False, "too many lines"
        if after.count('\n') == after.count("- ") > 10:
            return False, "too many items"
        if self.prompt_templates['base'] and self.prompt_templates['base'] in after:
            return False, "prompt leaked 1"
        if "#New Prompt#" in after:
            return False, "prompt leaked 2"
        if "new prompt" in after.lower():
            return False, "prompt leaked 3"
        if "how can i assist" in after.lower():
            return False, "AI"
        if "as an ai" in after.lower():
            return False, "AI"
        if "gpt" in after.lower() and "gpt" not in before.lower():
            return False, "AI"        
        if "ai assistant" in after.lower():
            return False, "AI"
        if "i'm sorry" in after.lower() and "sorry" not in before.lower() and len(after) < 400:
            return False, "sorry"
        if False:
            # too slow in general, not needed
            prompt = """Are the two following prompts equal to each other?
To be equal, they must meet two requirements:
1. Both prompts have the same constraints and requirements.
2. Both prompts have the same depth and breath of the inquiry.
First prompt: %s
Second prompt: %s
Answer with 'Equal' or 'Not Equal'. No need to explain the reason.""" % (before, after)
            answer = self.llm_pipeline(prompt)
            if 'not equal' not in answer.lower():
                return False, "equal"
        return True, "ok"


class AzureGPTPipeline:
    def __init__(self, model_name, **kwargs):
        self.model_name = model_name
        self.model_type = "aoai"
        self.kwargs = kwargs 
        self.client = AzureOpenAI(
            azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key        = os.getenv("AZURE_OPENAI_API_KEY"),
            api_version    = os.getenv("AZURE_OPENAI_API_VERSION")
        )
            
    def __call__(self, dataset, **kwargs):
        ret = []

        gen_count = 0
        for d in dataset:
            logger.info(f"Generating {gen_count+1} of {len(dataset)}")
            response = None
            retries = 0
            while not response and retries < MAX_RETRIES:
                try:
                    response = self.client.chat.completions.create(
                        model=self.model_name,
                        messages=[{"role": "user", "content": d['text']}],
                        **kwargs     
                    )
                except RateLimitError as e:
                    logger.info("Rate limit exceeded. Retrying in 10 seconds...")
                    retries += 1
                    time.sleep(10)
            if response:
                ret.append(response.choices[0].message.content)
            else:
                ret.append("")
            gen_count += 1
            if gen_count % 10 == 0:
                logger.info(gen_count)
        return ret

    def generateResponse(self, prompt: str, num_copies: int = 2) -> List[str]:
        if self.model_type == "aoai":
            return self.generateApi(prompt, num_copies)
        else:
            raise ValueError("Unsupported model_type.")
    
    def generateApi(self, prompt: str, num_rollouts) -> List[str]:
        def send_request(prompt):
            temperature = random.choice([0.7, 1.0])#(self.temperature_range)
            if self.model_type == "aoai":
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=self.kwargs["max_tokens"],
                    temperature=self.kwargs["temperature"]
                    # seed=
                )
                output = response.choices[0].message.content
            else:
                assert False, "only support azure open ai"
            return output

        responses = []
        with ThreadPoolExecutor(max_workers=num_rollouts) as executor:
            futures = [executor.submit(send_request, prompt) for _ in range(num_rollouts)]
            for future in tqdm(as_completed(futures), total=len(futures)):
                responses.append(future.result())

        return responses

import argparse
if __name__ == "__main__":
    defaultseedfile = os.path.join(os.path.dirname(__file__),'samples/math_500_tst.json')
    parser = argparse.ArgumentParser(description='Options')
    parser.add_argument("--seed_file", type=str, default=defaultseedfile)
    parser.add_argument("--column_names", default="problem") #Instruction
    parser.add_argument("--temperature", type=int, default=0.7)
    parser.add_argument("--top_p", type=int, default=0.95)
    parser.add_argument("--model_name", type=str, default="gpt-4o")
    parser.add_argument("--num_branches", type=int, default=4) # how many branches we should explore when we complete rest part of a solution base on the existing part.
    parser.add_argument("--max_search", type=int, default=4) # the max limit of times we try to explore different solution of a problem using a MCTS like method
    parser.add_argument("--max_branches", type=int, default=40) # the max limit of the total number of branches we have explored when search different solutions for a problem
    args = parser.parse_args()
    
    # global logger
    logger = setup_logging(args.seed_file)

    llm_pipeline = AzureGPTPipeline(
        args.model_name, 
        max_tokens=1024,
        temperature=args.temperature,
        top_p=args.top_p
    )

    wizardlm = WizardLM(
        llm_pipeline=llm_pipeline,
        seed_data=args.seed_file,
        column_names=args.column_names,
        num_rows=2,
        # min_len_chars=args.min_len_chars,
        # max_len_chars=args.max_len_chars,
        language="English",
        verbose=True,
        numBranches = args.num_branches,
        maxSrch = args.max_search,
        maxBranches = args.max_branches,
        saveAsTree = True
    )

    # if args.question_only: 
    wizardlm.runQuestionOnly() # no need to gen answer, as there are ground truth in seed datas.
    # else:
    #     wizardlm.run()