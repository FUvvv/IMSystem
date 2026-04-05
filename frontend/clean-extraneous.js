// clean-extraneous.js
const { execSync } = require('child_process');

try {
  // 1. 获取依赖树
  const result = execSync('npm ls --json', { encoding: 'utf8' });
  const data = JSON.parse(result);

  // 2. 遍历依赖，找出 extraneous
  const extraneous = [];
  function checkDeps(deps) {
    for (const [name, info] of Object.entries(deps || {})) {
      if (info.extraneous) {
        extraneous.push(name);
      }
      if (info.dependencies) {
        checkDeps(info.dependencies);
      }
    }
  }
  checkDeps(data.dependencies);

  // 3. 根据结果处理
  if (extraneous.length > 0) {
    console.log('检测到 extraneous 依赖:', extraneous.join(', '));
    // 一次性卸载
    execSync(`npm uninstall ${extraneous.join(' ')}`, { stdio: 'inherit' });
    console.log('已清理完成 ✅');
  } else {
    console.log('没有检测到 extraneous 依赖 🎉');
  }
} catch (err) {
  console.error('执行失败:', err.message);
}
