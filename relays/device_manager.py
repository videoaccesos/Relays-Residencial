# device_manager.py

import requests
from html.parser import HTMLParser
import xml.etree.ElementTree as ET

class HTMLRelayParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.states = {}
        self._in_div = False
        self._cur_id = None
        self._in_span = False

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for k, v in attrs:
                if k == 'id' and v.startswith('td'):
                    try:
                        self._cur_id = int(v[2:])
                        self._in_div = True
                    except:
                        pass
        elif self._in_div and tag == 'span':
            self._in_span = True

    def handle_data(self, data):
        if self._in_div and self._in_span and self._cur_id is not None:
            text = data.strip().lower()
            if text:
                self.states[self._cur_id] = 'On' if text.startswith('on') else 'Off'

    def handle_endtag(self, tag):
        if tag == 'span':
            self._in_span = False
        elif tag == 'div':
            self._in_div = False
            self._cur_id = None

class RelayDevice:
    """
    Genera la URL de control y parsea estados en HTML o XML
    según cfg['type'] y cfg['relays'][…]['cmd_template'].
    """

    def __init__(self, cfg):
        self.url_base  = cfg['url_base'].rstrip('/')
        self.dev_type  = cfg['type'].lower()          # 'html' o 'xml'
        self.auth      = tuple(cfg.get('auth', {}).values()) if cfg.get('auth') else None
        self.pw        = cfg.get('pw')
        self.cfg       = cfg

    def get_states(self):
        """Sólo lectura de estado, sin cambiar nada."""
        return self.set_and_get_states(None, None)

    def set_and_get_states(self, relay_id, new_state):
        """Si relay_id!=None hace el control, y luego siempre lee todos los estados."""
        if self.dev_type == 'html':
            return self._html_cycle(relay_id, new_state)
        else:
            return self._xml_cycle(relay_id, new_state)

    def _html_cycle(self, r, s):
        # 1) Ejecuta el comando si r no es None
        if r is not None:
            entry   = next((rl for rl in self.cfg['relays'] if rl['id']==r), {})
            tpl     = entry.get('cmd_template', f"?relay={r};st={s}")
            ctrl_url= f"{self.url_base}/{tpl.lstrip('?')}"
            requests.get(ctrl_url, auth=self.auth, timeout=5).raise_for_status()

        # 2) Descarga página principal y parsea con HTMLRelayParser
        resp = requests.get(self.url_base, auth=self.auth, timeout=5)
        resp.raise_for_status()
        parser = HTMLRelayParser()
        parser.feed(resp.text)
        return parser.states

    def _xml_cycle(self, r, s):
        base_xml = f"{self.url_base}/current_state.xml"
        # 1) Control si r no es None
        if r is not None:
            params = {f"Relay{r}": str(s)}
            if self.pw:
                params['pw'] = self.pw
            requests.get(base_xml, params=params, auth=self.auth, timeout=5).raise_for_status()

        # 2) Lectura de estados
        resp = requests.get(base_xml, auth=self.auth, timeout=5)
        resp.raise_for_status()
        root = ET.fromstring(resp.content)

        states = {}
        for node in root:
            if node.tag.startswith('Relay'):
                idx = int(node.tag.replace('Relay',''))
                st  = node.findtext('State','0').strip()
                states[idx] = 'On' if st!='0' else 'Off'
        return states
