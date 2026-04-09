第一次提交：
    1、创建数据库：inventory_db
    2、撰写Readme.md，记录工程框架、运行环境、环境配置、启动步骤
    3、实现基础框架

第二次提交：
    1、实现数据库连接
    2、完善商品管理
    3、完善用户管理
    4、完善库存管理

第三次提交：
    1、完善日志管理
    2、完善报表管理（不算太完善，导出格式无法修改，只能导出库存
    3、完善权限管理

第四次提交：
    1、修改系统日志界面日志类型下拉表宽度大小
    2、实现自定义模板的报表导出，包括xlsx格式与pdf格式（pdf格式只能英文，中文乱码，中文解决方案如下：
        第一步：准备中文字体文件
            建议使用开源免费的商用中文字体，以避免版权问题：

            下载字体：例如 阿里巴巴普惠体 (Alibaba PuHuiTi) 或 思源黑体 (Noto Sans SC)。
            解压后，找到 .ttf 格式的字体文件（例如 NotoSansSC-Regular.ttf）。
            注意：尽量选择体积较小的常规体（Regular），因为字体文件会增加最终打包的体积。
        第二步：将 TTF 字体转换为 Base64 格式
            jsPDF 官方提供了一个在线转换工具，可以将 .ttf 文件转换为 js 代码：

            打开 jsPDF 官方字体转换工具：jsPDF Font Converter
            点击 "选择文件" 选择你的 .ttf 字体文件。
            在 "fontName" 输入框中为你的字体起个英文名字（例如输入 NotoSans）。
            点击 "Create" 按钮，它会生成一个 .js 文件并自动下载。
            这个生成的 .js 文件内部其实就是将字体转换成了 Base64 字符串，并调用了 addFileToVFS。

        第三步：在项目中引入生成的字体文件
            将下载的 .js 文件（例如 NotoSans-normal.js）放到你的 Vue 项目中，比如放到 src/assets/fonts/ 目录下。
            打开这个 .js 文件，你可能会看到类似这样的代码：
            JAVASCRIPT
            import { jsPDF } from "jspdf"
            var font = "AAEAAAARAQAABAAQRkZUTW...很长的Base64...";
            var callAddFont = function () {
            this.addFileToVFS("NotoSans-normal.ttf", font);
            this.addFont("NotoSans-normal.ttf", "NotoSans", "normal");
            };
            jsPDF.API.events.push(['addFonts', callAddFont])
            (如果你的项目是基于 Vite/Webpack 的模块化项目，建议直接将那个很长的 Base64 字符串提取出来，用下面的方式手动注册，更利于控制。)
        第四步：修改 Vue 代码，手动注册并应用中文字体
            假设你已经拿到了字体的 Base64 字符串。修改你代码中的 exportToPDF 函数：

            JAVASCRIPT
            // 1. 引入你的字体 Base64 字符串（你可以把字符串单独放到一个 js 文件里 export 出来导入）
            // import { NotoSansBase64 } from '@/assets/fonts/NotoSansBase64.js'
            // 这里为了演示，用一个变量代替
            const NotoSansBase64 = "AAEAAAARAQAABAAQRkZUTW...这里替换为你转换出的真实Base64字符串...";

            const exportToPDF = (exportData, reportTitle) => {
            const doc = new jsPDF()
            
            // 2. 将字体添加到 jsPDF 的虚拟文件系统中
            doc.addFileToVFS('NotoSans-normal.ttf', NotoSansBase64)
            
            // 3. 注册字体 (文件名, 字体名, 字体样式)
            doc.addFont('NotoSans-normal.ttf', 'NotoSans', 'normal')
            
            // 4. 设置全局默认字体为刚注册的中文字体
            doc.setFont('NotoSans')

            // --- 下面的绘制代码不需要大改，只要保证设置了字体即可 ---
            
            doc.setFontSize(18)
            doc.text("XX集团有限公司", 105, 15, { align: "center" })
            
            doc.setFontSize(14)
            doc.text(reportTitle, 105, 25, { align: "center" })
            
            doc.setFontSize(10)
            doc.text(`报表编号: REP-${new Date().getTime()}`, 14, 35)
            doc.text(`生成时间: ${new Date().toLocaleString()}`, 14, 42)
            doc.text(`导出部门: 数据中心`, 140, 35)
            doc.text(`导出人: Admin`, 140, 42)

            const tableHeaders = Object.keys(exportData[0])
            const tableData = exportData.map(item => Object.values(item))

            // 5. 在 autoTable 中配置样式，指定使用刚才注册的中文字体
            autoTable(doc, {
                startY: 50,
                head: [tableHeaders],
                body: tableData,
                theme: 'grid',
                headStyles: { fillColor: [64, 158, 255] },
                styles: { 
                font: 'NotoSans', // 这里的名字必须和 doc.addFont 的第二个参数一致
                fontSize: 10 
                }
            })

            const finalY = doc.lastAutoTable.finalY || 50
            doc.text("制表人：______________   审核人：______________   批准人：______________", 14, finalY + 20)

            doc.save(`${reportTitle}_${new Date().getTime()}.pdf`)
            }
        总结关键点：
            获取 .ttf 并转成 Base64。
            使用 doc.addFileToVFS 注入 Base64。
            使用 doc.addFont 注册字体名称。
            使用 doc.setFont('你的字体名') 让普通 doc.text() 支持中文。
            在 autoTable 的配置项 styles: { font: '你的字体名' } 中指定字体，让表格支持中文。
        问题在于Base64过长，cpu储存不足，其路径在"G:\AAA IMSystem\资源\Noto_Sans_SC\src\assets\fonts\NotoSansBase64.js"

第五次修改：
    1、登陆界面添加用户注册，管理员只能重置密码为123456；
    2、添加商品属性：商品规格、生产日期、批号（批号生成算法随意，与日期相关即可），同步修改报表导出选项和数据库初始化代码；
    3、商品管理页面添加模糊查询按钮与显示全部按钮，并实现相应功能；

第六次修改：
    1、将密码存储改为哈希存储

