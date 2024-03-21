module.exports = {
    root: true,
    env: {
      node: true,
    },
    'extends': [
      'plugin:vue/vue3-essential', // Vue 2の場合は 'plugin:vue/essential'
      'eslint:recommended',
      '@vue/typescript/recommended' // TypeScriptを使用する場合
    ],
    parserOptions: {
      ecmaVersion: 2020,
    },
    rules: {
      // カスタムルール
    },
  };
  