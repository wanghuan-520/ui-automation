import * as fs from 'fs';
import * as path from 'path';

/**
 * 生成一个指定大小的PNG图片文件
 * 通过创建大尺寸的位图数据来达到目标文件大小
 */
class ImageGenerator {
  /**
   * 生成10M的图片文件
   */
  static async generate10MBImage(outputPath: string): Promise<void> {
    try {
      // 目标文件大小: 10MB = 10 * 1024 * 1024 bytes
      const targetSize = 10 * 1024 * 1024;
      
      console.log(`开始生成 ${targetSize} 字节的图片文件...`);
      
      // 创建一个简单的位图格式 (BMP)
      // BMP格式更容易控制文件大小
      const width = 2000;
      const height = 1667; // 约2000x1667的图片，每像素3字节RGB，约10MB
      
      // BMP文件头 (14字节)
      const fileHeader = Buffer.alloc(14);
      fileHeader.write('BM', 0); // BMP标识
      fileHeader.writeUInt32LE(targetSize, 2); // 文件大小
      fileHeader.writeUInt32LE(54, 10); // 像素数据偏移
      
      // BMP信息头 (40字节)
      const infoHeader = Buffer.alloc(40);
      infoHeader.writeUInt32LE(40, 0); // 信息头大小
      infoHeader.writeUInt32LE(width, 4); // 图片宽度
      infoHeader.writeUInt32LE(height, 8); // 图片高度
      infoHeader.writeUInt16LE(1, 12); // 颜色平面数
      infoHeader.writeUInt16LE(24, 14); // 每像素位数 (24位RGB)
      infoHeader.writeUInt32LE(0, 16); // 压缩方式 (0=不压缩)
      infoHeader.writeUInt32LE(targetSize - 54, 20); // 像素数据大小
      
      // 创建像素数据
      const pixelDataSize = targetSize - 54;
      const pixelData = Buffer.alloc(pixelDataSize);
      
      // 生成渐变色彩数据，让图片看起来有内容
      for (let i = 0; i < pixelDataSize; i += 3) {
        const position = i / pixelDataSize;
        pixelData[i] = Math.floor(255 * Math.sin(position * Math.PI * 4)); // Blue
        pixelData[i + 1] = Math.floor(255 * Math.cos(position * Math.PI * 6)); // Green  
        pixelData[i + 2] = Math.floor(255 * Math.sin(position * Math.PI * 8)); // Red
      }
      
      // 合并所有数据
      const imageBuffer = Buffer.concat([fileHeader, infoHeader, pixelData]);
      
      // 确保文件大小正好是10MB
      const finalBuffer = Buffer.alloc(targetSize);
      imageBuffer.copy(finalBuffer, 0, 0, Math.min(imageBuffer.length, targetSize));
      
      // 写入文件
      await fs.promises.writeFile(outputPath, finalBuffer);
      
      // 验证文件大小
      const stats = await fs.promises.stat(outputPath);
      const actualSize = stats.size;
      const sizeMB = (actualSize / (1024 * 1024)).toFixed(2);
      
      console.log(`✅ 图片生成成功！`);
      console.log(`📁 文件路径: ${outputPath}`);
      console.log(`📊 文件大小: ${actualSize} 字节 (${sizeMB} MB)`);
      console.log(`🎨 图片尺寸: ${width} x ${height} 像素`);
      console.log(`🌈 格式: BMP (24位真彩色)`);
      
    } catch (error) {
      console.error('❌ 生成图片时发生错误:', error);
      throw error;
    }
  }
}

// 主函数
async function main() {
  const outputPath = path.join(__dirname, 'test-images', '10mb-test-image.bmp');
  
  // 确保输出目录存在
  const outputDir = path.dirname(outputPath);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  await ImageGenerator.generate10MBImage(outputPath);
}

// 如果直接运行此脚本
if (require.main === module) {
  main().catch(console.error);
}

export { ImageGenerator }; 