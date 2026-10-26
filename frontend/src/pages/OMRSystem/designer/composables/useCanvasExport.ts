import { printOmrElement } from '../../utils/omrPrint'

export function useCanvasExport() {
  async function printSheet(config: any, presentationMode: string) {
    const svgEl = (
      document.querySelector('.sheet-artboard-container svg.yemeni-ministry-sheet-svg') ||
      document.querySelector('.sheet-artboard-container svg.yemeni-sheet-svg') ||
      document.querySelector('.sheet-artboard-container svg[viewBox="0 0 210 148.5"]') ||
      document.querySelector('.sheet-artboard-container svg[viewBox="0 0 210 297"]') ||
      document.querySelector('.sheet-artboard-container svg.omr-svg') ||
      document.querySelector('.sheet-artboard-container svg')
    ) as SVGGraphicsElement

    if (svgEl) {
      await printOmrElement(svgEl, {
        title: config?.template_name || 'OMR_Sheet',
        isA5: presentationMode === 'compact_a5',
      })
    } else {
      window.print()
    }
  }

  async function exportPNG(config: any) {
    const svgEl = (
      document.querySelector('.sheet-artboard-container svg.yemeni-ministry-sheet-svg') ||
      document.querySelector('.sheet-artboard-container svg.yemeni-sheet-svg') ||
      document.querySelector('.sheet-artboard-container svg[viewBox="0 0 210 148.5"]') ||
      document.querySelector('.sheet-artboard-container svg[viewBox="0 0 210 297"]') ||
      document.querySelector('.sheet-artboard-container svg.omr-svg') ||
      document.querySelector('.sheet-artboard-container svg')
    ) as SVGGraphicsElement

    if (!svgEl) {
      console.error('No SVG element found to export')
      return
    }

    try {
      const clonedSvg = svgEl.cloneNode(true) as SVGGraphicsElement
      clonedSvg.setAttribute('xmlns', 'http://www.w3.org/2000/svg')
      clonedSvg.setAttribute('xmlns:xlink', 'http://www.w3.org/1999/xlink')

      const viewBox = svgEl.getAttribute('viewBox') || '0 0 210 148.5'
      const parts = viewBox.trim().split(/[\s,]+/).map(Number)
      const vbWidth = parts[2] || 210
      const vbHeight = parts[3] || 148.5

      const dpi = 600
      const targetWidth = Math.round(vbWidth * (dpi / 25.4))
      const targetHeight = Math.round(vbHeight * (dpi / 25.4))

      clonedSvg.setAttribute('width', `${targetWidth}`)
      clonedSvg.setAttribute('height', `${targetHeight}`)
      clonedSvg.style.width = `${targetWidth}px`
      clonedSvg.style.height = `${targetHeight}px`

      const images = Array.from(clonedSvg.querySelectorAll('image'))
      for (const imgEl of images) {
        const href = imgEl.getAttribute('href') || imgEl.getAttribute('xlink:href') || ''
        if (href && !href.startsWith('data:')) {
          try {
            const fullUrl = href.startsWith('http') ? href : `${window.location.origin}${href}`
            const resp = await fetch(fullUrl)
            if (resp.ok) {
              const blob = await resp.blob()
              const b64 = await new Promise<string>((resolve, reject) => {
                const reader = new FileReader()
                reader.onloadend = () => resolve(reader.result as string)
                reader.onerror = reject
                reader.readAsDataURL(blob)
              })
              imgEl.setAttribute('href', b64)
              imgEl.removeAttribute('xlink:href')
            }
          } catch (e) {
            console.warn('Could not inline image for export:', href, e)
          }
        }
      }

      const serializer = new XMLSerializer()
      const svgStr = serializer.serializeToString(clonedSvg)

      const blob = new Blob([svgStr], { type: 'image/svg+xml;charset=utf-8' })
      const url = URL.createObjectURL(blob)

      const img = new Image()
      img.onload = () => {
        const canvas = document.createElement('canvas')
        canvas.width = targetWidth
        canvas.height = targetHeight
        const ctx = canvas.getContext('2d')
        if (ctx) {
          ctx.imageSmoothingEnabled = true
          ctx.imageSmoothingQuality = 'high'
          ctx.fillStyle = '#ffffff'
          ctx.fillRect(0, 0, canvas.width, canvas.height)
          ctx.drawImage(img, 0, 0, targetWidth, targetHeight)

          const pngUrl = canvas.toDataURL('image/png', 1.0)
          const a = document.createElement('a')
          a.href = pngUrl
          a.download = `${config?.template_name || 'OMR_Sheet'}_600DPI_UltraHD.png`
          document.body.appendChild(a)
          a.click()
          document.body.removeChild(a)
        }
        URL.revokeObjectURL(url)
      }
      img.onerror = (e) => {
        console.error('Image load error during export:', e)
        URL.revokeObjectURL(url)
      }
      img.src = url
    } catch (err) {
      console.error('Export PNG failed:', err)
    }
  }

  function exportJson(config: any) {
    try {
      const jsonStr = JSON.stringify(config, null, 2)
      const blob = new Blob([jsonStr], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `${config?.template_id || 'template'}_config.json`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    } catch (e) {
      console.error('Export JSON failed:', e)
    }
  }

  return {
    printSheet,
    exportPNG,
    exportJson,
  }
}
