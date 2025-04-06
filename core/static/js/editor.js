window.runHTMLCode = function () {
  let html = "";

  // Если подключён CodeMirror
  if (window.htmlEditor) {
    html = window.htmlEditor.getValue();
  } else {
    const textarea = document.getElementById("code-html");
    if (!textarea) {
      alert("❌ Элемент с id='code-html' не найден!");
      return;
    }
    html = textarea.value;
  }

  const iframe = document.getElementById("preview");
  if (!iframe) {
    alert("❌ iframe с id='preview' не найден!");
    return;
  }

  console.log("📥 Получен HTML-код:", html);

  const fullHTML = `
    <!DOCTYPE html>
    <html>
      <head><meta charset="UTF-8"></head>
      <body>${html}</body>
    </html>
  `;

  const blob = new Blob([fullHTML], { type: 'text/html' });
  const blobURL = URL.createObjectURL(blob);

  iframe.src = blobURL;

  // iframe.onload = () => {
  //   console.log("✅ iframe загружен");

  //   try {
  //     const doc = iframe.contentDocument || iframe.contentWindow.document;
  //     const actualOutput = doc.body.innerText.replace(/\s+/g, ' ').trim();
  //     const expectedOutput = window.codeExpectedOutput.replace(/\s+/g, ' ').trim();

  //     console.log("🔍 Сравнение результата:");
  //     console.log("  👉 Ожидалось:", expectedOutput);
  //     console.log("  👉 Получено:", actualOutput);

  //     if (actualOutput === expectedOutput) {
  //       console.log("🎉 Совпадение! Урок выполнен.");
  //       markLessonAsCompleted();
  //     } else {
  //       alert("⚠ Результат не совпадает с ожидаемым. Проверь код.");
  //     }
  //   } catch (err) {
  //     console.error("❌ Ошибка чтения из iframe:", err);
  //     alert("Произошла ошибка при проверке результата.");
  //   }

  //   setTimeout(() => URL.revokeObjectURL(blobURL), 1000);
  // };
};

iframe.onload = () => {
  console.log("✅ iframe загружен");

  try {
    const doc = iframe.contentDocument || iframe.contentWindow.document;

    // Получаем чистый текст без лишних пробелов и переносов
    const actualOutput = doc.body.innerText.replace(/\s+/g, ' ').trim().toLowerCase();
    const expectedOutput = window.codeExpectedOutput.replace(/\s+/g, ' ').trim().toLowerCase();

    console.log("🔍 Сравнение результата:");
    console.log("  👉 Ожидалось:", expectedOutput);
    console.log("  👉 Получено:", actualOutput);

    // Строгое, но очищенное текстовое сравнение
    if (actualOutput === expectedOutput) {
      console.log("🎉 Совпадение! Урок выполнен.");
      markLessonAsCompleted();
    } else {
      console.warn("⚠ Результат отличается.");
      alert("Результат не совпадает с ожидаемым. Убедитесь, что текст и структура верны.");
    }
  } catch (err) {
    console.error("❌ Ошибка при чтении из iframe:", err);
    alert("Произошла ошибка при проверке результата.");
  }

  setTimeout(() => URL.revokeObjectURL(blobURL), 1000);
};

function markLessonAsCompleted() {
  console.log("📌 Урок завершён (заглушка)");
}
