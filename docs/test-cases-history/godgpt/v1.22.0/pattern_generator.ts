import * as fs from 'fs';
import * as path from 'path';

// 生成指定模式的字符序列 - 精确500K字符版本
function generatePattern(): string {
    // 定义字符集：数字 + 小写字母 + 大写字母 = 62个字符
    const characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    
    // 精确计算重复次数以达到准确的500,000字符
    // 500,000 ÷ 62 = 8064.516...
    // 前32个字符重复8065次，后30个字符重复8064次
    // 验证：32 × 8065 + 30 × 8064 = 258,080 + 241,920 = 500,000
    const baseRepeatCount = 8064; // 基础重复次数
    const extraRepeatCount = 8065; // 额外重复次数
    const extraCharCount = 32; // 需要额外重复的字符数量
    
    let result = '';
    
    console.log('开始生成精确500K字符模式...');
    console.log('字符集大小:', characters.length);
    console.log(`前${extraCharCount}个字符重复次数:`, extraRepeatCount);
    console.log(`后${characters.length - extraCharCount}个字符重复次数:`, baseRepeatCount);
    console.log('预期总字符数: 500,000');

    // 对每个字符进行处理
    for (let i = 0; i < characters.length; i++) {
        const char = characters[i];
        // 根据位置决定重复次数
        const repeatCount = i < extraCharCount ? extraRepeatCount : baseRepeatCount;
        // 重复当前字符指定次数
        result += char.repeat(repeatCount);
        
        // 进度提示（每10个字符输出一次）
        if ((i + 1) % 10 === 0) {
            console.log(`已处理 ${i + 1}/${characters.length} 个字符`);
        }
    }

    console.log('模式生成完成！');
    return result;
}

// 将生成的模式写入文件
function writePatternToFile(pattern: string, filename: string): void {
    try {
        const outputPath = path.join(__dirname, filename);
        console.log(`正在写入文件: ${outputPath}`);
        
        fs.writeFileSync(outputPath, pattern, 'utf8');
        
        console.log(`文件写入成功！`);
        console.log(`文件路径: ${outputPath}`);
        console.log(`文件大小: ${(fs.statSync(outputPath).size / 1024).toFixed(2)} KB`);
    } catch (error) {
        console.error('文件写入失败:', error);
    }
}

// 导出函数以供测试使用
export { generatePattern, writePatternToFile };

// 主函数用于测试
function main() {
    const startTime = Date.now();
    const pattern = generatePattern();
    const endTime = Date.now();
    
    console.log('\n=== 生成结果统计 ===');
    console.log('实际生成的模式长度:', pattern.length);
    console.log('生成耗时:', (endTime - startTime) + 'ms');
    console.log('是否达到500K字符:', pattern.length >= 500000 ? '是' : '否');
    
    // 输出前100个字符作为样例
    console.log('\n前100个字符样例:');
    console.log(pattern.substring(0, 100));
    
    // 输出最后100个字符作为样例
    console.log('\n最后100个字符样例:');
    console.log(pattern.substring(pattern.length - 100));
    
    // 生成文件名（包含时间戳）
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filename = `pattern-500k-${timestamp}.txt`;
    
    // 将结果写入文件
    console.log('\n=== 文件输出 ===');
    writePatternToFile(pattern, filename);
}

// 如果直接运行此文件则执行主函数
if (require.main === module) {
    main();
} 