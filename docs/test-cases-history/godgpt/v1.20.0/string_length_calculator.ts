// 字符串长度计算器

/**
 * 使用直接长度计算
 * @param str 输入字符串
 * @returns 字符串长度
 */
export function calculateDirectLength(str: string): number {
    return str.length;
}

/**
 * 使用正则表达式匹配连续字符
 * @param str 输入字符串
 * @returns 字符串长度
 */
export function calculateRegexLength(str: string): number {
    const zeros = str.match(/0+/)?.[0]?.length || 0;
    const ones = str.match(/1+/)?.[0]?.length || 0;
    return zeros + ones;
}

/**
 * 使用数组reduce方法计数
 * @param str 输入字符串
 * @returns 字符串长度
 */
export function calculateReduceLength(str: string): number {
    return str.split('').reduce((acc) => acc + 1, 0);
}

/**
 * 使用字符分组统计
 * @param str 输入字符串
 * @returns 包含每种字符数量的对象
 */
export function calculateGroupLength(str: string): { zeros: number; ones: number; total: number } {
    const zeros = (str.match(/0/g) || []).length;
    const ones = (str.match(/1/g) || []).length;
    return {
        zeros,
        ones,
        total: zeros + ones
    };
}

/**
 * 使用二进制特性计算
 * @param str 输入字符串
 * @returns 包含2的幂次方信息的结果
 */
export function calculateBinaryPowerLength(str: string): { 
    zerosCount: number;
    onesCount: number;
    zerosPower: number;
    onesPower: number;
    total: number;
} {
    const zerosCount = (str.match(/0/g) || []).length;
    const onesCount = (str.match(/1/g) || []).length;
    
    // 计算最接近的2的幂次方
    const zerosPower = Math.log2(zerosCount);
    const onesPower = Math.log2(onesCount);

    return {
        zerosCount,
        onesCount,
        zerosPower,
        onesPower,
        total: zerosCount + onesCount
    };
}

import * as fs from 'fs';
import * as path from 'path';

// 计算文件中的字符数量
async function calculateStringLength(filePath: string): Promise<number> {
    try {
        // 读取文件内容
        const content = await fs.promises.readFile(filePath, 'utf8');
        // 返回字符数量
        return content.length;
    } catch (error) {
        console.error('读取文件时发生错误:', error);
        throw error;
    }
}

// 主函数
async function main() {
    const filePath = path.join(__dirname, 'input-test-110000.txt');
    try {
        const length = await calculateStringLength(filePath);
        console.log('文件中的字符数量:', length);
    } catch (error) {
        console.error('程序执行出错:', error);
    }
}

// 执行主函数
main(); 