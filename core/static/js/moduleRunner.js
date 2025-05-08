document.addEventListener('DOMContentLoaded', () => {
    console.log('Runner: DOMContentLoaded');
    const htmlEditor = window.htmlEditor;
    const jsEditor   = window.jsEditor;
    const btn        = document.getElementById('runBtn');
    const preview    = document.getElementById('preview');
    const feedback   = document.getElementById('feedback');
  
    function parseExpectedFromHtml(html) {
      const wrapper = document.createElement('div');
      wrapper.innerHTML = html;
      return (wrapper.textContent || '').trim();
    }
  
    btn.addEventListener('click', () => {
      console.log('Runner: Launch clicked');
      feedback.textContent = '';
  
      const userHtml = htmlEditor.getValue();
      const userJs   = jsEditor.getValue();
      console.log('Runner: userHtml =', userHtml);
      console.log('Runner: userJs =', userJs);
  
      // Определяем expected
      const expected = window.expectedOutput != null
        ? String(window.expectedOutput).trim()
        : parseExpectedFromHtml(userHtml);
      console.log('Runner: expected =', expected);
  
      // Повешаем onload до srcdoc
      preview.onload = () => {
        console.log('Runner: iframe onload');
        try {
          const doc = preview.contentDocument;
          console.log('Runner: got contentDocument:', !!doc);
  
          // inject user JS
          const s1 = doc.createElement('script');
          s1.textContent = userJs;
          doc.body.appendChild(s1);
          console.log('Runner: user JS injected');
  
          // inject check script
          const s2 = doc.createElement('script');
          s2.textContent = `
            (function(){
              const out = (document.getElementById('output')?.innerText || '').trim();
              console.log('Runner(iframe): out =', out);
              parent.postMessage(out, '*');
            })();
          `;
          doc.body.appendChild(s2);
          console.log('Runner: check script injected');
        } catch (err) {
          console.error('Runner: injection error', err);
        }
      };
  
      // Загружаем HTML
      preview.srcdoc = `
        <html><head><meta charset="utf-8"></head>
        <body>${userHtml}</body>
        </html>
      `;
      console.log('Runner: srcdoc set');
    });
  
    window.addEventListener('message', (e) => {
      console.log('Runner: message received', e.data);
      const got = (e.data || '').trim();
      const expected = window.expectedOutput != null
        ? String(window.expectedOutput).trim()
        : parseExpectedFromHtml(htmlEditor.getValue());
  
      if (got === expected) {
        feedback.innerHTML = '<span class="text-green-400">✅ Верно!</span>';
      } else {
        feedback.innerHTML = `<span class="text-red-400">❌ Неверно. Ожидалось: “${expected}”, получено: “${got}”</span>`;
      }
    });
  });
  