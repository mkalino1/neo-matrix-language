<template>
  <div class="neo-editor">
    <div class="main-content">
      <div class="editor-section">
        <div class="section-title">Code Editor</div>
        <textarea ref="codeEditor" id="codeEditor"></textarea>
        <button class="run-button" @click="runCode" :disabled="isRunning" id="runButton">
          ▶ {{ isRunning ? 'Running...' : 'Run Code' }}
        </button>
        <div class="loading" v-if="isRunning">
          <div class="spinner"></div>
          <div>Executing code...</div>
        </div>
      </div>
      
      <div class="output-section">
        <div class="section-title">Output</div>
        <div class="output-area" id="outputArea">
          {{ output || '# Output will appear here after running your code' }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'

// Reactive data
const isRunning = ref(false)
const output = ref('')
const codeEditor = ref(null)
let editor = null

// Initialize CodeMirror after component mounts
onMounted(async () => {
  await nextTick()
  
  // Check if CodeMirror is available
  if (typeof CodeMirror === 'undefined') {
    // Load CodeMirror dynamically if not available
    await loadCodeMirror()
  }
  
  // Initialize editor
  editor = CodeMirror.fromTextArea(document.getElementById("codeEditor"), {
    mode: "javascript", // We'll use JavaScript mode as a base
    theme: "monokai",
    lineNumbers: true,
    autoCloseBrackets: true,
    matchBrackets: true,
    indentUnit: 4,
    tabSize: 4,
    lineWrapping: true,
    extraKeys: {
      "Tab": function(cm) {
        cm.replaceSelection("    ", "end");
      }
    }
  });

  // Set default code
  editor.setValue(`# Welcome to Neo Matrix Language!
# Try running this example:

func greet(name) {
    print("Hello, " + name + "!");
}

greet("World");`);

  // Handle Ctrl+Enter to run code
  editor.on("keydown", function(cm, event) {
    if (event.ctrlKey && event.keyCode === 13) { // Ctrl+Enter
      event.preventDefault();
      runCode();
    }
  });
})

// Load CodeMirror dynamically
async function loadCodeMirror() {
  // Load CSS
  const link = document.createElement('link')
  link.rel = 'stylesheet'
  link.href = 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/codemirror.min.css'
  document.head.appendChild(link)
  
  const themeLink = document.createElement('link')
  themeLink.rel = 'stylesheet'
  themeLink.href = 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/theme/monokai.min.css'
  document.head.appendChild(themeLink)
  
  // Load JavaScript
  const script = document.createElement('script')
  script.src = 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/codemirror.min.js'
  document.head.appendChild(script)
  
  // Wait for script to load
  return new Promise((resolve) => {
    script.onload = resolve
  })
}

// Run code function
async function runCode() {
  if (!editor) return
  
  const code = editor.getValue();
  
  if (!code.trim()) {
    output.value = "# Please enter some code to execute";
    return;
  }

  // Show loading state
  isRunning.value = true;
  output.value = "# Executing code...";

  try {
    const response = await fetch('/api/execute', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ code: code })
    });

    const data = await response.json();

    if (data.success) {
      let result = "";
      if (data.output) {
        result += data.output;
      }
      if (data.result && data.result !== "None") {
        result += "\n# Return value: " + data.result;
      }
      output.value = result || "# Code executed successfully (no output)";
    } else {
      output.value = "# Error: " + data.error;
      if (data.traceback) {
        output.value += "\n\n# Traceback:\n" + data.traceback;
      }
    }
  } catch (error) {
    output.value = "# Network error: " + error.message;
  } finally {
    // Hide loading state
    isRunning.value = false;
  }
}
</script>

<style scoped>
.neo-editor {
  margin: 2rem 0;
}

.main-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0;
  min-height: 600px;
}

.editor-section {
  padding: 20px;
}

.output-section {
  padding: 20px;
}

.section-title {
  font-size: 1.3em;
  margin-bottom: 15px;
  font-weight: 600;
}

:deep(.CodeMirror) {
  height: 400px;
  border-radius: 8px;
  font-size: 14px;
}

.run-button {
  color: white;
  background-color: #272822;
  border: none;
  padding: 12px 30px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 15px;
  transition: all 0.3s ease;
}

.run-button:hover:not(:disabled) {
  background-color: #373832;
  transform: translateY(-1px);
}

.run-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.output-area {
  background: #272822;
  padding: 15px;
  border-radius: 8px;
  font-family: 'Courier New', monospace;
  font-size: 13px;
  line-height: 1.5;
  min-height: 400px;
  white-space: pre-wrap;
  overflow-y: auto;
}

.loading {
  text-align: center;
  padding: 20px;
  color: #667eea;
}

.spinner {
  border: 3px solid #f3f3f3;
  border-top: 3px solid #667eea;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  animation: spin 1s linear infinite;
  margin: 0 auto 10px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .main-content {
    grid-template-columns: 1fr;
  }
}
</style>
