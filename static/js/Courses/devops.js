document.addEventListener("DOMContentLoaded", () => {
  const contentViewer = document.getElementById("content-viewer");
  const contentLinks = document.querySelectorAll(".content-link");
  const contentHeader = document.getElementById("content-header"); // The right panel header
  const sidebar = document.getElementById("sidebar");
  const mainContent = document.getElementById("main-content");

  // Sidebar toggle functionality
  const toggleSidebar = document.getElementById("toggle-sidebar");
  toggleSidebar.addEventListener("click", () => {
    sidebar.classList.toggle("closed");
    mainContent.classList.toggle("fullscreen");
  });

  // Toggle subtitle content visibility
  window.toggleContent = (subtitleId) => {
    const content = document.getElementById(`content-links-${subtitleId}`);
    content.style.display = content.style.display === "none" ? "block" : "none";
  };

  // Display selected video, PDF, or notes in the content viewer
  contentLinks.forEach((link) => {
    link.addEventListener("click", (event) => {
      event.preventDefault();
      const contentType = link.dataset.type;
      const contentTitle = link.dataset.title;
      const contentUrl = link.dataset.url;
      const contentData = link.dataset.content; // For notes

      // Hide the content header (Welcome message)
      contentHeader.style.display = "none";

      // Update content viewer with selected content
      contentViewer.innerHTML = `        
        <h2>${contentTitle}</h2>
        ${
          contentType === "video"
            ? `<div class="video-container">
                <video controls>
                  <source src="${contentUrl}" type="video/mp4">
                  Your browser does not support the video tag.
                </video>
              </div>`
            : contentType === "pdf"
            ? `<div id="pdf-controls">
                <button id="prev-page">Previous</button>
                <span id="current-page">1</span> / <span id="page-count"></span>
                <button id="next-page">Next</button>
                <button id="fullscreen-toggle">Full Screen</button>
              </div>
              <div id="pdf-container">
                <canvas id="pdf-canvas"></canvas>
              </div>`
            : `<div class="notes-container">
                ${contentData}
              </div>`
        }
      `;

      // If PDF is selected, render it using pdf.js
      if (contentType === "pdf") {
        const canvas = document.getElementById("pdf-canvas");
        const context = canvas.getContext("2d");
        const loadingTask = pdfjsLib.getDocument(contentUrl);
        let pdfDoc = null;
        let currentPage = 1;

        loadingTask.promise
          .then((pdf) => {
            pdfDoc = pdf;
            document.getElementById("page-count").textContent = pdf.numPages;
            renderPage(currentPage);
          })
          .catch((error) => {
            console.error("Error loading PDF:", error);
            contentViewer.innerHTML = `<p>Error loading PDF. Please try again later.</p>`;
          });

        function renderPage(pageNum) {
          pdfDoc.getPage(pageNum).then((page) => {
            const viewport = page.getViewport({ scale: 1 });
            canvas.width = viewport.width;
            canvas.height = viewport.height;
            const renderContext = {
              canvasContext: context,
              viewport: viewport,
            };
            page.render(renderContext);
            document.getElementById("current-page").textContent = pageNum;
          });
        }

        document.getElementById("prev-page").addEventListener("click", () => {
          if (currentPage > 1) {
            currentPage--;
            renderPage(currentPage);
          }
        });

        document.getElementById("next-page").addEventListener("click", () => {
          if (currentPage < pdfDoc.numPages) {
            currentPage++;
            renderPage(currentPage);
          }
        });

        // Fullscreen toggle functionality for PDF
        const fullscreenButton = document.getElementById("fullscreen-toggle");
        fullscreenButton.addEventListener("click", () => {
          const pdfContainer = document.getElementById("pdf-container");
          if (!document.fullscreenElement) {
            pdfContainer.requestFullscreen();
          } else {
            document.exitFullscreen();
          }
        });
      }
    });
  });
});
