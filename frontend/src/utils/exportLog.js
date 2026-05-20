import html2canvas from "html2canvas";
import { jsPDF } from "jspdf";

export async function exportLogAsPng(element, filename) {
  const canvas = await html2canvas(element, { scale: 2, backgroundColor: "#fff" });
  const link = document.createElement("a");
  link.download = filename;
  link.href = canvas.toDataURL("image/png");
  link.click();
}

export async function exportLogAsPdf(element, filename) {
  const canvas = await html2canvas(element, { scale: 2, backgroundColor: "#fff" });
  const img = canvas.toDataURL("image/png");
  const pdf = new jsPDF({ orientation: "landscape", unit: "pt", format: "letter" });
  const pageWidth = pdf.internal.pageSize.getWidth();
  const pageHeight = (canvas.height * pageWidth) / canvas.width;
  pdf.addImage(img, "PNG", 0, 10, pageWidth, pageHeight);
  pdf.save(filename);
}
