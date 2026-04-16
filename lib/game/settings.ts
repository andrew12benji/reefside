// settings.ts — Game settings with localStorage persistence

const STORAGE_KEY = "reefside_settings";

interface KeyMap {
  left: string;
  right: string;
  up: string;
  ability: string;
  pause: string;
  sound: string;
}

interface Settings {
  keyMap: KeyMap;
  colorblind: string;
  soundEnabled: boolean;
}

const DEFAULTS: Settings = {
  keyMap: {
    left: "KeyA",
    right: "KeyD",
    up: "KeyW",
    ability: "KeyE",
    pause: "KeyP",
    sound: "KeyM",
  },
  colorblind: "none", // 'none' | 'deuteranopia' | 'protanopia' | 'tritanopia'
  soundEnabled: false,
};

function load(): Settings {
  if (typeof window === "undefined") {
    return { ...DEFAULTS, keyMap: { ...DEFAULTS.keyMap } };
  }
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { ...DEFAULTS, keyMap: { ...DEFAULTS.keyMap } };
    const parsed = JSON.parse(raw);
    return {
      ...DEFAULTS,
      ...parsed,
      keyMap: { ...DEFAULTS.keyMap, ...(parsed.keyMap || {}) },
    };
  } catch {
    return { ...DEFAULTS, keyMap: { ...DEFAULTS.keyMap } };
  }
}

function save(s: Settings): void {
  if (typeof window === "undefined") return;
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(s));
  } catch {
    // Ignore localStorage errors
  }
}

let _cache: Settings | null = null;

export function getSettings(): Settings {
  if (!_cache) _cache = load();
  return _cache;
}

export function setSettings(partial: Partial<Settings>): Settings {
  _cache = { ...getSettings(), ...partial };
  if (partial.keyMap)
    _cache.keyMap = { ...getSettings().keyMap, ...partial.keyMap };
  save(_cache);
  return _cache;
}

export function resetSettings(): Settings {
  _cache = { ...DEFAULTS, keyMap: { ...DEFAULTS.keyMap } };
  save(_cache);
  return _cache;
}

export function getKeyMap(): KeyMap {
  return getSettings().keyMap;
}

// Human-readable key names
export function keyCodeLabel(code: string): string {
  const map: Record<string, string> = {
    Space: "SPACE",
    Enter: "ENTER",
    Escape: "ESC",
    ShiftLeft: "L-SHIFT",
    ShiftRight: "R-SHIFT",
    ControlLeft: "L-CTRL",
    ControlRight: "R-CTRL",
    AltLeft: "L-ALT",
    AltRight: "R-ALT",
    Tab: "TAB",
    ArrowLeft: "LEFT",
    ArrowRight: "RIGHT",
    ArrowUp: "UP",
    ArrowDown: "DOWN",
  };
  if (map[code]) return map[code];
  if (code.startsWith("Key")) return code.slice(3);
  if (code.startsWith("Digit")) return code.slice(5);
  if (code.startsWith("Numpad")) return "NP" + code.slice(6);
  if (code.startsWith("F")) return code;
  return code;
}

export type { Settings, KeyMap };
