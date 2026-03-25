#!/usr/bin/env node

/**
 * 周易起卦辅助脚本
 * 用法：node generate-gua.mjs [问题] [--method coin|number] [--verbose]
 */

function usage() {
  console.error(`
周易起卦工具

Usage: generate-gua.mjs "your question" [options]

Options:
  -m, --method coin|number   起卦方法 (default: number)
  -v, --verbose             显示详细解读
  -h, --help               显示帮助信息

Examples:
  node generate-gua.mjs "我是否应该跳槽"
  node generate-gua.mjs "事业发展的趋势如何" --method coin --verbose
`);
  process.exit(2);
}

// 八卦基础数据
const BAGUA = {
  1: { name: '乾', symbol: '☰', element: '天', binary: '111' },
  2: { name: '兑', symbol: '☱', element: '泽', binary: '110' },
  3: { name: '离', symbol: '☲', element: '火', binary: '101' },
  4: { name: '震', symbol: '☳', element: '雷', binary: '100' },
  5: { name: '巽', symbol: '☴', element: '风', binary: '011' },
  6: { name: '坎', symbol: '☵', element: '水', binary: '010' },
  7: { name: '艮', symbol: '☶', element: '山', binary: '001' },
  8: { name: '坤', symbol: '☷', element: '地', binary: '000' }
};

// 六十四卦名称速查表 (简化版)
const HEXAGRAMS = {
  '111111': { name: '乾为天', meaning: '刚健自强、开创进取' },
  '000000': { name: '坤为地', meaning: '柔顺包容、厚德载物' },
  '111001': { name: '水天需', meaning: '等待时机、蓄势待发' },
  '111010': { name: '天水讼', meaning: '争端化解、寻求平衡' },
  '010000': { name: '地水师', meaning: '组织纪律、选对领袖' },
  '000010': { name: '水地比', meaning: '亲密合作、建立联盟' },
  '100111': { name: '风天小畜', meaning: '小有积蓄、等待时机' },
  '011111': { name: '天泽履', meaning: '小心行事、以柔克刚' },
  '111011': { name: '地天泰', meaning: '阴阳和合、通达顺利' },
  '101111': { name: '天地否', meaning: '闭塞不通、需要变革' }
  // 完整六十四卦需补充，此处为简化演示
};

function generateYao() {
  // 模拟硬币法：3 个硬币抛掷
  const coins = [Math.random() > 0.5, Math.random() > 0.5, Math.random() > 0.5];
  
  const positiveCount = coins.filter(c => c).length;
  
  if (positiveCount === 3) return { type: '少阴', symbol: '- -', movable: false };
  if (positiveCount === 2) return { type: '少阳', symbol: '——', movable: false };
  if (positiveCount === 1) return { type: '老阳', symbol: 'O', movable: true };
  return { type: '老阴', symbol: 'X', movable: true };
}

function generateHexagram() {
  const yao = [];
  
  for (let i = 0; i < 6; i++) {
    yao.push(generateYao());
  }
  
  return yao; // 从下往上，index 0 是初爻
}

function identifyHexagram(yao) {
  // 根据六个爻识别卦名（简化版）
  const binary = yao.map(yl => {
    if (yl.type === '少阳' || yl.type === '老阳') return '1';
    return '0';
  }).join('');
  
  return HEXAGRAMS[binary] || { name: '未知卦', meaning: '需要查阅完整卦表' };
}

function printYao(yao, index) {
  const names = ['初', '二', '三', '四', '五', '上'];
  const yaoType = yao[index].type === '阳' || yao[index].type === '少阳' ? '阳' : '阴';
  
  console.log(`${names[index]}${yaoType}: ${yao[index].symbol} ${yao[index].movable ? '(变爻)' : ''}`);
}

function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args[0] === '-h' || args[0] === '--help') {
    usage();
  }
  
  // 解析参数
  let question = '未指定问题';
  let method = 'number';
  let verbose = false;
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '-m' || args[i] === '--method') {
      method = args[++i] || 'number';
    } else if (args[i] === '-v' || args[i] === '--verbose') {
      verbose = true;
    } else if (!args[i].startsWith('-')) {
      question = args[i];
    }
  }
  
  console.log('='.repeat(50));
  console.log('         🎯 周易起卦工具 v1.0');
  console.log('='.repeat(50));
  console.log();
  
  // 显示问题
  console.log(`📝 问题：${question}`);
  console.log();
  
  // 生成卦象
  const yao = generateHexagram();
  const hexagram = identifyHexagram(yao);
  
  // 显示卦形
  console.log('🔮 卦象（从下往上）:');
  console.log('┌─────────────────────┐');
  for (let i = 5; i >= 0; i--) {
    const symbol = yao[i].symbol === '——' ? '━━━' : 
                   yao[i].symbol === '- -' ? '─ ─' :
                   yao[i].symbol === 'O' ? '〇〇' : '××';
    console.log(`│  ${yao[i].type.padEnd(4)} | ${symbol}`);
  }
  console.log('└─────────────────────┘');
  console.log();
  
  // 显示卦名和含义
  console.log(`📖 卦名：${hexagram.name}`);
  console.log(`💡 核心含义：${hexagram.meaning}`);
  console.log();
  
  // 检查变爻
  const movableYao = yao.map((yl, idx) => yl.movable ? idx + 1 : null).filter(v => v !== null);
  
  if (movableYao.length > 0) {
    console.log(`🔄 变爻位置：第${movableYao.join('、第')}爻`);
    console.log('   （表示事情可能会有变化，需要特别关注）');
    console.log();
  }
  
  if (verbose) {
    console.log('📋 详细爻辞:');
    yao.forEach((yl, idx) => printYao(yao, idx));
    console.log();
  }
  
  // 显示解读建议
  console.log('='.repeat(50));
  console.log('💭 解读建议：');
  console.log(`1. 这个卦象反映了"${question}"这个问题的大方向`);
  console.log(`2. 核心关键词是：${hexagram.meaning.split('、')[0]}`);
  console.log(`3. ${movableYao.length > 0 ? '有变爻，说明事情可能会有转折点' : '无变爻，事情按当前趋势发展'}`);
  console.log(`4. 建议结合现实情况具体分析，不要盲目迷信`);
  console.log('='.repeat(50));
  
  console.log();
  console.log('📚 提示：如需详细解读，请查阅 references/六十四卦.md');
}

main();