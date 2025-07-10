import * as fs from 'fs';
import * as path from 'path';
import {
    calculateDirectLength,
    calculateRegexLength,
    calculateReduceLength,
    calculateGroupLength,
    calculateBinaryPowerLength
} from './string_length_calculator';

// 读取测试文件
const testFilePath = path.join(__dirname, 'input-test-putong.txt');
const content = fs.readFileSync(testFilePath, 'utf-8');

console.log('字符串长度计算结果：');
console.log('-'.repeat(50));

// 1. 直接长度计算
const directLength = calculateDirectLength(content);
console.log('1. 直接长度计算:', directLength);

// 2. 正则表达式匹配
const regexLength = calculateRegexLength(content);
console.log('2. 正则表达式匹配:', regexLength);

// 3. Reduce方法计算
const reduceLength = calculateReduceLength(content);
console.log('3. Reduce方法计算:', reduceLength);

// 4. 字符分组统计
const groupResult = calculateGroupLength(content);
console.log('4. 字符分组统计:');
console.log('   - 0的数量:', groupResult.zeros);
console.log('   - 1的数量:', groupResult.ones);
console.log('   - 总数量:', groupResult.total);

// 5. 二进制特性计算
const binaryResult = calculateBinaryPowerLength(content);
console.log('5. 二进制特性计算:');
console.log('   - 0的数量:', binaryResult.zerosCount, `(2^${binaryResult.zerosPower})`);
console.log('   - 1的数量:', binaryResult.onesCount, `(2^${binaryResult.onesPower})`);
console.log('   - 总数量:', binaryResult.total);

console.log('-'.repeat(50));
console.log('验证: 所有方法计算结果是否一致:');
const results = [
    directLength,
    regexLength,
    reduceLength,
    groupResult.total,
    binaryResult.total
];
const isConsistent = results.every(r => r === results[0]);
console.log('结果一致性:', isConsistent ? '✅ 所有结果相同' : '❌ 结果不一致'); 