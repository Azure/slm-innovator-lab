targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name of the the environment which is used to generate a short unique hash used in all resources.')
param environmentName string

@minLength(1)
@description('Primary location for all resources')
@allowed(['eastus', 'westus2', 'northcentralus'])
@metadata({
  azd: {
    type: 'location'
  }
})
param location string

param resourceGroupName string = '' // Set in main.parameters.json

@secure()
param openAiServiceName string = ''

param useGPT4V bool = false

@description('Location for the OpenAI resource group')
@allowed([
  'canadaeast'
  'eastus'
  'eastus2'
  'francecentral'
  'switzerlandnorth'
  'uksouth'
  'japaneast'
  'northcentralus'
  'australiaeast'
  'swedencentral'
])
@metadata({
  azd: {
    type: 'location'
  }
})
param openAiResourceGroupLocation string

param azureOpenAiSkuName string = '' // Set in main.parameters.json

param documentIntelligenceServiceName string = '' // Set in main.parameters.json

param applicationInsightsName string = '' // Set in main.parameters.json
param logAnalyticsName string = '' // Set in main.parameters.json

param storageAccountName string = '' // Set in main.parameters.json
param storageSkuName string // Set in main.parameters.json

param keyVaultName string = '' // Set in main.parameters.json

param documentIntelligenceSkuName string // Set in main.parameters.json

param azureOpenAiDeploymentName string = '' // Set in main.parameters.json
param azureOpenAiDeploymentSkuName string = '' // Set in main.parameters.json
param azureOpenAiDeploymentVersion string = '' // Set in main.parameters.json
param azureOpenAiDeploymentCapacity int = 0 // Set in main.parameters.json
var gpt4omini = {
  modelName: 'gpt-4o-mini'
  deploymentName: !empty(azureOpenAiDeploymentName) ? azureOpenAiDeploymentName : 'gpt-4o-mini'
  deploymentVersion: !empty(azureOpenAiDeploymentVersion) ? azureOpenAiDeploymentVersion : '2024-07-18'
  deploymentSkuName: !empty(azureOpenAiDeploymentSkuName) ? azureOpenAiDeploymentSkuName : 'Standard'
  deploymentCapacity: azureOpenAiDeploymentCapacity != 0 ? azureOpenAiDeploymentCapacity : 30
}

param embeddingModelName string = ''
param embeddingDeploymentName string = ''
param embeddingDeploymentVersion string = ''
param embeddingDeploymentSkuName string = ''
param embeddingDeploymentCapacity int = 0
param embeddingDimensions int = 0
var embedding = {
  modelName: !empty(embeddingModelName) ? embeddingModelName : 'text-embedding-ada-002'
  deploymentName: !empty(embeddingDeploymentName) ? embeddingDeploymentName : 'embedding'
  deploymentVersion: !empty(embeddingDeploymentVersion) ? embeddingDeploymentVersion : '2'
  deploymentSkuName: !empty(embeddingDeploymentSkuName) ? embeddingDeploymentSkuName : 'Standard'
  deploymentCapacity: embeddingDeploymentCapacity != 0 ? embeddingDeploymentCapacity : 30
  dimensions: embeddingDimensions != 0 ? embeddingDimensions : 1536
}

param gpt4vModelName string = ''
param gpt4vDeploymentName string = ''
param gpt4vModelVersion string = ''
param gpt4vDeploymentSkuName string = ''
param gpt4vDeploymentCapacity int = 0
var gpt4v = {
  modelName: !empty(gpt4vModelName) ? gpt4vModelName : 'gpt-4o'
  deploymentName: !empty(gpt4vDeploymentName) ? gpt4vDeploymentName : 'gpt-4o'
  deploymentVersion: !empty(gpt4vModelVersion) ? gpt4vModelVersion : '2024-05-13'
  deploymentSkuName: !empty(gpt4vDeploymentSkuName) ? gpt4vDeploymentSkuName : 'Standard'
  deploymentCapacity: gpt4vDeploymentCapacity != 0 ? gpt4vDeploymentCapacity : 10
}

param tenantId string = tenant().tenantId

@allowed(['None', 'AzureServices'])
@description('If allowedIp is set, whether azure services are allowed to bypass the storage and AI services firewall.')
param bypass string = 'AzureServices'

@description('Public network access value for all deployed resources')
@allowed(['Enabled', 'Disabled'])
param publicNetworkAccess string = 'Enabled'

var abbrs = loadJsonContent('abbreviations.json')
var resourceToken = toLower(uniqueString(subscription().id, environmentName, location))
var tags = { 'azd-env-name': environmentName }

// Organize resources in a resource group
resource resourceGroup 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: !empty(resourceGroupName) ? resourceGroupName : '${abbrs.resourcesResourceGroups}${environmentName}'
  location: location
  tags: tags
}

var defaultOpenAiDeployments = [
  {
    name: gpt4omini.deploymentName
    model: {
      format: 'OpenAI'
      name: gpt4omini.modelName
      version: gpt4omini.deploymentVersion
    }
    sku: {
      name: gpt4omini.deploymentSkuName
      capacity: gpt4omini.deploymentCapacity
    }
  }
  {
    name: embedding.deploymentName
    model: {
      format: 'OpenAI'
      name: embedding.modelName
      version: embedding.deploymentVersion
    }
    sku: {
      name: embedding.deploymentSkuName
      capacity: embedding.deploymentCapacity
    }
  }
]

var openAiDeployments = concat(
  defaultOpenAiDeployments,
  useGPT4V
    ? [
        {
          name: gpt4v.deploymentName
          model: {
            format: 'OpenAI'
            name: gpt4v.modelName
            version: gpt4v.deploymentVersion
          }
          sku: {
            name: gpt4v.deploymentSkuName
            capacity: gpt4v.deploymentCapacity
          }
        }
      ]
    : []
)

module vault 'br/public:avm/res/key-vault/vault:0.10.1' = {
  name: 'keyvault'
  scope: resourceGroup
  params: {
    name: !empty(keyVaultName) ? keyVaultName : '${abbrs.keyVaultVaults}${resourceToken}'
    tags: tags
    enablePurgeProtection: false
    enableRbacAuthorization: true
    location: location
    enableSoftDelete: false
    networkAcls: {
      bypass: bypass
      defaultAction: 'Deny'
    }
  }
}

module openAi 'br/public:avm/res/cognitive-services/account:0.7.2' = {
  name: 'openai'
  scope: resourceGroup
  params: {
    name: '${abbrs.cognitiveServicesAccounts}${resourceToken}'
    location: openAiResourceGroupLocation
    tags: tags
    kind: 'OpenAI'
    customSubDomainName: !empty(openAiServiceName)
      ? openAiServiceName
      : '${abbrs.cognitiveServicesAccounts}${resourceToken}'
    publicNetworkAccess: publicNetworkAccess
    networkAcls: {
      defaultAction: 'Allow'
      bypass: bypass
    }
    sku: azureOpenAiSkuName
    deployments: openAiDeployments
    disableLocalAuth: true
    managedIdentities: {
      systemAssigned: true
    }
    secretsExportConfiguration: {
      accessKey1Name: 'openai-api-key1'
      accessKey2Name: 'openai-api-key2'
      keyVaultResourceId: vault.outputs.resourceId
    }
  }
}

module storageAccount 'br/public:avm/res/storage/storage-account:0.14.1' = {
  name: 'storage'
  scope: resourceGroup
  params: {
    name: !empty(storageAccountName) ? storageAccountName : '${abbrs.storageStorageAccounts}${resourceToken}'
    kind: 'BlobStorage'
    publicNetworkAccess: publicNetworkAccess
    allowBlobPublicAccess: false
    allowSharedKeyAccess: false
    location: location
    tags: tags
    skuName: storageSkuName
    networkAcls: {
      bypass: bypass
      defaultAction: 'Deny'
    }
  }
}

module workspace 'br/public:avm/res/operational-insights/workspace:0.7.0' = {
  name: 'loganalytics'
  scope: resourceGroup
  params: {
    name: !empty(logAnalyticsName) ? logAnalyticsName : '${abbrs.logAnayticsWorkspace}${resourceToken}'
    location: location
    tags: tags
    publicNetworkAccessForIngestion: publicNetworkAccess
  }
}

module appinsights 'br/public:avm/res/insights/component:0.4.1' = {
  name: 'appinsights'
  scope: resourceGroup
  params: {
    name: !empty(applicationInsightsName) ? applicationInsightsName : '${abbrs.insightsComponents}${resourceToken}'
    workspaceResourceId: workspace.outputs.resourceId
    location: location
    tags: tags
    publicNetworkAccessForIngestion: publicNetworkAccess
  }
}

module mlworkspace 'br/public:avm/res/machine-learning-services/workspace:0.8.1' = {
  name: 'mlworkspace'
  scope: resourceGroup
  params: {
    name: '${abbrs.machineLearningServicesWorkspaces}${resourceToken}'
    sku: 'Basic'
    associatedApplicationInsightsResourceId: appinsights.outputs.resourceId
    associatedKeyVaultResourceId: vault.outputs.resourceId
    associatedStorageAccountResourceId: storageAccount.outputs.resourceId
    location: location
    tags: tags
  }
}

// Formerly known as Form Recognizer
// Does not support bypass
module documentIntelligence 'br/public:avm/res/cognitive-services/account:0.7.2' = {
  name: 'documentintelligence'
  scope: resourceGroup
  params: {
    name: '${abbrs.cognitiveServicesDocumentIntelligence}${resourceToken}'
    kind: 'FormRecognizer'
    customSubDomainName: !empty(documentIntelligenceServiceName)
      ? documentIntelligenceServiceName
      : '${abbrs.cognitiveServicesDocumentIntelligence}${resourceToken}'
    publicNetworkAccess: publicNetworkAccess
    networkAcls: {
      defaultAction: 'Allow'
    }
    location: location
    disableLocalAuth: true
    tags: tags
    sku: documentIntelligenceSkuName
  }
}

output AZURE_LOCATION string = location
output AZURE_TENANT_ID string = tenantId
output AZURE_RESOURCE_GROUP string = resourceGroup.name

// Shared by all OpenAI deployments
output AZURE_OPENAI_EMB_MODEL_NAME string = embedding.modelName
output AZURE_OPENAI_OPENAI_MODEL string = gpt4omini.modelName
output AZURE_OPENAI_GPT4V_MODEL string = gpt4v.modelName

// Specific to Azure OpenAI
output AZURE_OPENAI_SERVICE_NAME string = openAi.outputs.name
output AZURE_OPENAI_DEPLOYMENT_NAME string = gpt4omini.deploymentName
output AZURE_OPENAI_EMB_DEPLOYMENT_NAME string = embedding.deploymentName
output AZURE_OPENAI_GPT4V_DEPLOYMENT_NAME string = gpt4v.deploymentName
output AZURE_DOCUMENTINTELLIGENCE_SERVICE string = documentIntelligence.outputs.name

// Output for the labs
output AZURE_OPENAI_ENDPOINT string = openAi.outputs.endpoint
output AZURE_OPENAI_API_KEY object = openAi.outputs.exportedSecrets

output AZURE_DOC_INTELLIGENCE_ENDPOINT string = documentIntelligence.outputs.endpoint
output AZURE_DOC_INTELLIGENCE_KEY_REFERENCE object = documentIntelligence.outputs.exportedSecrets
