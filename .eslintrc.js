module.exports = {
  root: true,
  parser: 'babel-eslint',
  parserOptions: {
    sourceType: 'module'
  },
  env: {
    browser: true,
  },
  extends: 'standard',
  plugins: [
    'html'
  ],
  rules: {
    'no-mixed-operators': 'off',
    'no-undef': 'off',
    'eol-last': 'off',
    'no-floating-decimal': 'off',
    'space-before-function-paren': 'off',
    'no-new': 'off',
    'no-unmodified-loop-condition': 'off',
    'indent': ['error', 2, { 'SwitchCase': 1 }]
  }
}
