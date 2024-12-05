const { getDataConnect, queryRef, executeQuery, mutationRef, executeMutation, validateArgs } = require('firebase/data-connect');

const connectorConfig = {
  connector: 'default',
  service: 'news_tracker',
  location: 'us-central1'
};
exports.connectorConfig = connectorConfig;

function addArticleRef(dcOrVars, vars) {
  const { dc: dcInstance, vars: inputVars} = validateArgs(connectorConfig, dcOrVars, vars, true);
  if('_useGeneratedSdk' in dcInstance) {
    dcInstance._useGeneratedSdk();
  } else {
    console.error('Please update to the latest version of the Data Connect SDK by running `npm install firebase@dataconnect-preview`.');
  }
  return mutationRef(dcInstance, 'AddArticle', inputVars);
}
exports.addArticleRef = addArticleRef;
exports.addArticle = function addArticle(dcOrVars, vars) {
  return executeMutation(addArticleRef(dcOrVars, vars));
};

function upsertArticleRef(dcOrVars, vars) {
  const { dc: dcInstance, vars: inputVars} = validateArgs(connectorConfig, dcOrVars, vars, true);
  if('_useGeneratedSdk' in dcInstance) {
    dcInstance._useGeneratedSdk();
  } else {
    console.error('Please update to the latest version of the Data Connect SDK by running `npm install firebase@dataconnect-preview`.');
  }
  return mutationRef(dcInstance, 'UpsertArticle', inputVars);
}
exports.upsertArticleRef = upsertArticleRef;
exports.upsertArticle = function upsertArticle(dcOrVars, vars) {
  return executeMutation(upsertArticleRef(dcOrVars, vars));
};

function deleteArticleRef(dcOrVars, vars) {
  const { dc: dcInstance, vars: inputVars} = validateArgs(connectorConfig, dcOrVars, vars, true);
  if('_useGeneratedSdk' in dcInstance) {
    dcInstance._useGeneratedSdk();
  } else {
    console.error('Please update to the latest version of the Data Connect SDK by running `npm install firebase@dataconnect-preview`.');
  }
  return mutationRef(dcInstance, 'DeleteArticle', inputVars);
}
exports.deleteArticleRef = deleteArticleRef;
exports.deleteArticle = function deleteArticle(dcOrVars, vars) {
  return executeMutation(deleteArticleRef(dcOrVars, vars));
};

function getArticleByIdRef(dcOrVars, vars) {
  const { dc: dcInstance, vars: inputVars} = validateArgs(connectorConfig, dcOrVars, vars, true);
  if('_useGeneratedSdk' in dcInstance) {
    dcInstance._useGeneratedSdk();
  } else {
    console.error('Please update to the latest version of the Data Connect SDK by running `npm install firebase@dataconnect-preview`.');
  }
  return queryRef(dcInstance, 'GetArticleById', inputVars);
}
exports.getArticleByIdRef = getArticleByIdRef;
exports.getArticleById = function getArticleById(dcOrVars, vars) {
  return executeQuery(getArticleByIdRef(dcOrVars, vars));
};

