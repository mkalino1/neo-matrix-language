<template>
  <div class="neo-editor">
    <div class="section-header">
      <h3 class="section-title">Code Editor</h3>
      <button class="run-button" @click="runCode" :disabled="isRunning" id="runButton">
        <svg v-if="!isRunning" class="icon" viewBox="0 0 24 24" fill="currentColor">
          <path d="M8 5v14l11-7z"/>
        </svg>
        <svg v-else class="icon spinner" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
        </svg>
        {{ isRunning ? 'Running...' : 'Run Code' }}
      </button>
    </div>
    <div class="editor-container">
      <textarea ref="codeEditor" id="codeEditor"></textarea>
    </div>
    <div class="loading" v-if="isRunning">
      <div class="loading-content">
        <div class="spinner"></div>
        <span>Executing code...</span>
      </div>
    </div>
  
    <div class="section-header">
      <h3 class="section-title">Output</h3>
    </div>
    <div class="output-container">
      <div class="output-area" id="outputArea">
        {{ output || '# Output will appear here after running your code' }}
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
    print("Hello, " + name + "!")
}

greet("World")`);

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
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  background: var(--vp-c-bg);
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
  display: flex;
  flex-direction: column;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.8rem 1.5rem;
  background: var(--vp-c-bg-soft);
  border-bottom: 1px solid var(--vp-c-divider);
}

.section-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0;
  color: var(--vp-c-text-1);
}

.editor-container, 
.output-container {
  padding: 1.5rem;
  background: var(--vp-c-bg);
}

:deep(.CodeMirror) {
  height: 350px;
  border-radius: 8px;
  font-size: 14px;
  border: 1px solid var(--vp-c-divider);
}

:deep(.CodeMirror-focused) {
  border-color: var(--vp-c-brand-1);
  box-shadow: 0 0 0 2px var(--vp-c-brand-1-soft);
}

.run-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: white;
  background: var(--vp-c-brand-1);
  border: 1px solid var(--vp-c-brand-1);
  padding: 4px 12px;
  border-radius: 10px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  
  &:hover:not(:disabled) {
    background: var(--vp-c-brand-2);
    border-color: var(--vp-c-brand-2);
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }
  
  &:focus-visible {
    outline: 2px solid var(--vp-c-brand-1);
    outline-offset: 2px;
  }
  
  .icon {
    width: 16px;
    height: 16px;
  }
  
  .spinner {
    animation: spin 1s linear infinite;
  }
}

.dark .run-button {
  color: black;
}

.output-area {
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  padding: 1rem;
  border-radius: 8px;
  font-family: var(--vp-font-mono);
  font-size: 0.875rem;
  line-height: 1.6;
  min-height: 200px;
  white-space: pre-wrap;
  overflow-y: auto;
  color: var(--vp-c-text-1);
}

.loading {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(2px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  
  .loading-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
    color: var(--vp-c-brand-1);
    font-weight: 500;
  }
  
  .spinner {
    width: 24px;
    height: 24px;
    border: 2px solid var(--vp-c-divider);
    border-top: 2px solid var(--vp-c-brand-1);
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }
}

.dark .loading {
  background: rgba(0, 0, 0, 0.8);
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .editor-container,
  .output-container {
    padding: 1rem;
  }
  
  :deep(.CodeMirror) {
    height: 250px;
  }
  
  .output-area {
    min-height: 150px;
  }
}
</style>
