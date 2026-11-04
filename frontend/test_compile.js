const { compileTemplate } = require('@vue/compiler-sfc');
const res = compileTemplate({
  source: '<custom-data-table-with-save :="{ headers: headers, items: items }" />',
  id: 'test',
  filename: 'test.vue'
});
console.log('CODE:\n', res.code);
console.log('ERRORS:\n', res.errors);

