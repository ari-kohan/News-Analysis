const { getDataConnect, queryRef, executeQuery, mutationRef, executeMutation, validateArgs } = require('firebase/data-connect');

const connectorConfig = {
  connector: 'default',
  service: 'articles-dataconnect',
  location: 'us-west1'
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

function addArticleAnalysisRef(dcOrVars, vars) {
  const { dc: dcInstance, vars: inputVars} = validateArgs(connectorConfig, dcOrVars, vars, true);
  if('_useGeneratedSdk' in dcInstance) {
    dcInstance._useGeneratedSdk();
  } else {
    console.error('Please update to the latest version of the Data Connect SDK by running `npm install firebase@dataconnect-preview`.');
  }
  return mutationRef(dcInstance, 'AddArticleAnalysis', inputVars);
}
exports.addArticleAnalysisRef = addArticleAnalysisRef;
exports.addArticleAnalysis = function addArticleAnalysis(dcOrVars, vars) {
  return executeMutation(addArticleAnalysisRef(dcOrVars, vars));
};

function deleteArticleAnalysisRef(dcOrVars, vars) {
  const { dc: dcInstance, vars: inputVars} = validateArgs(connectorConfig, dcOrVars, vars);
  if('_useGeneratedSdk' in dcInstance) {
    dcInstance._useGeneratedSdk();
  } else {
    console.error('Please update to the latest version of the Data Connect SDK by running `npm install firebase@dataconnect-preview`.');
  }
  return mutationRef(dcInstance, 'DeleteArticleAnalysis', inputVars);
}
exports.deleteArticleAnalysisRef = deleteArticleAnalysisRef;
exports.deleteArticleAnalysis = function deleteArticleAnalysis(dcOrVars, vars) {
  return executeMutation(deleteArticleAnalysisRef(dcOrVars, vars));
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

function getArticleAnalysisByIdRef(dcOrVars, vars) {
  const { dc: dcInstance, vars: inputVars} = validateArgs(connectorConfig, dcOrVars, vars, true);
  if('_useGeneratedSdk' in dcInstance) {
    dcInstance._useGeneratedSdk();
  } else {
    console.error('Please update to the latest version of the Data Connect SDK by running `npm install firebase@dataconnect-preview`.');
  }
  return queryRef(dcInstance, 'GetArticleAnalysisById', inputVars);
}
exports.getArticleAnalysisByIdRef = getArticleAnalysisByIdRef;
exports.getArticleAnalysisById = function getArticleAnalysisById(dcOrVars, vars) {
  return executeQuery(getArticleAnalysisByIdRef(dcOrVars, vars));
};

function getAllArticlesRef(dc) {
  const { dc: dcInstance} = validateArgs(connectorConfig, dc, undefined);
  if('_useGeneratedSdk' in dcInstance) {
    dcInstance._useGeneratedSdk();
  } else {
    console.error('Please update to the latest version of the Data Connect SDK by running `npm install firebase@dataconnect-preview`.');
  }
  return queryRef(dcInstance, 'GetAllArticles');
}
exports.getAllArticlesRef = getAllArticlesRef;
exports.getAllArticles = function getAllArticles(dc) {
  return executeQuery(getAllArticlesRef(dc));
};

function searchArticlesRef(dcOrVars, vars) {
  const { dc: dcInstance, vars: inputVars} = validateArgs(connectorConfig, dcOrVars, vars, true);
  if('_useGeneratedSdk' in dcInstance) {
    dcInstance._useGeneratedSdk();
  } else {
    console.error('Please update to the latest version of the Data Connect SDK by running `npm install firebase@dataconnect-preview`.');
  }
  return queryRef(dcInstance, 'SearchArticles', inputVars);
}
exports.searchArticlesRef = searchArticlesRef;
exports.searchArticles = function searchArticles(dcOrVars, vars) {
  return executeQuery(searchArticlesRef(dcOrVars, vars));
};

