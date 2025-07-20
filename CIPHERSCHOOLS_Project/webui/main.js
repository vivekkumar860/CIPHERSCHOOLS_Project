// List of targets (can be extended)
const targets = [
  {
    name: "Acunetix PHP (testphp.vulnweb.com)",
    url: "http://testphp.vulnweb.com/userinfo.php",
    username: "test",
    username_field: "uname",
    password_field: "pass",
    success_indicator: "John Smith",
    failure_indicator: "you must login"
  },
  {
    name: "Acunetix HTML5 (testhtml5.vulnweb.com)",
    url: "http://testhtml5.vulnweb.com/login.php",
    username: "admin",
    username_field: "username",
    password_field: "password",
    success_indicator: "welcome",
    failure_indicator: "invalid"
  },
  {
    name: "DVWA (localhost)",
    url: "http://localhost/dvwa/login.php",
    username: "admin",
    username_field: "username",
    password_field: "password",
    success_indicator: "Welcome to Damn Vulnerable Web Application",
    failure_indicator: "Login failed"
  }
];

function populateTargets() {
  const select = document.getElementById('target');
  targets.forEach((t, i) => {
    const opt = document.createElement('option');
    opt.value = i;
    opt.textContent = t.name;
    select.appendChild(opt);
  });
  select.selectedIndex = 0;
  fillFormFromTarget(0);
}

function fillFormFromTarget(idx) {
  const t = targets[idx];
  document.getElementById('username').value = t.username;
  document.getElementById('usernameField').value = t.username_field;
  document.getElementById('passwordField').value = t.password_field;
  document.getElementById('successIndicator').value = t.success_indicator;
  document.getElementById('failureIndicator').value = t.failure_indicator;
}

document.addEventListener('DOMContentLoaded', () => {
  populateTargets();
  document.getElementById('target').addEventListener('change', e => {
    fillFormFromTarget(e.target.value);
  });
  document.getElementById('downloadBtn').addEventListener('click', downloadConfig);
});

function downloadConfig() {
  const idx = document.getElementById('target').value;
  const t = targets[idx];
  const config = {
    url: t.url,
    username: document.getElementById('username').value,
    username_field: document.getElementById('usernameField').value,
    password_field: document.getElementById('passwordField').value,
    success_indicator: document.getElementById('successIndicator').value,
    failure_indicator: document.getElementById('failureIndicator').value,
    threads: parseInt(document.getElementById('threads').value, 10),
    timeout: parseInt(document.getElementById('timeout').value, 10),
    delay: parseInt(document.getElementById('delay').value, 10),
    progress_interval: parseInt(document.getElementById('progressInterval').value, 10)
  };
  const yaml = toYAML(config);
  const blob = new Blob([yaml], {type: 'text/yaml'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'config.yaml';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

// Simple YAML generator (for this config structure)
function toYAML(obj) {
  let out = '';
  for (const k in obj) {
    out += `${k}: "${String(obj[k]).replace(/"/g, '\"')}"\n`;
  }
  return out;
} 