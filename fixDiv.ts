import { readdir, readFile, writeFile } from 'fs/promises'
import { join } from 'path'

const htmlDir = './posts'
const outputDir = './output'

async function findFiles(folderPath: string) {
  return await readdir(folderPath)
}

function fixContent(fileContent: string) {
  const rewriter = new HTMLRewriter().on('body', {
    element(el) {
      el.append(
        '</div>',
        { html: true }
      )
    }
  })

  const result = rewriter.transform(fileContent)
  return result
}

function centerImage(fileContent: string) {
  const matchPattern = /<div>\s*(<img[^>]*>)\s*<\/div>/g
  return fileContent.replace(matchPattern, (_match, imgTag) => `<div class='img-wrapper'>${imgTag}</div>`);
}

async function fixFiles(htmlDir: string) {
  const files = await findFiles(htmlDir)

  for (const file of files) {
    if (!file.endsWith('.html')) continue

    const filePath = join(htmlDir, file)
    const fileContent = await readFile(filePath, 'utf-8')
    const fixedHTML = fixContent(fileContent)
    const fixedImage = centerImage(fixedHTML)

    const newFilePath = join(outputDir, file)

    await writeFile(newFilePath, fixedImage, 'utf-8');
    console.log('processed: ', file)
  }
}

fixFiles(htmlDir)