// 生成指定模式的字符序列
function generatePattern(): string {
    // 定义字符集
    const characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const repeatCount = 161; // 每个字符重复的次数
    let result = '';

    // 对每个字符进行处理
    for (let char of characters) {
        // 重复当前字符指定次数
        result += char.repeat(repeatCount);
    }

    return result;
}

// 导出函数以供测试使用
export { generatePattern };

// 主函数用于测试
function main() {
    const pattern = generatePattern();
    console.log('生成的模式长度:', pattern.length);
    console.log('\n完整的模式内容:');
    console.log(pattern);
}

// 如果直接运行此文件则执行主函数
if (require.main === module) {
    main();
} 