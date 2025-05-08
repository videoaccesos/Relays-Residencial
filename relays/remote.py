from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from device_manager import RelayDevice
from config import CONFIG

remote_bp = Blueprint('remote', __name__)

@remote_bp.route('/remote')
@login_required
def remote_panel():
    if current_user.role != 'operator':
        return 'Acceso denegado', 403
    return render_template('operator.html')

@remote_bp.route('/api/residences')
@login_required
def api_list_residences():
    if current_user.role != 'operator':
        return jsonify(error='Forbidden'), 403
    # Sólo enviamos id y nombre para poblar el select
    data = [
        {'id': r['id'], 'name': r['name']}
        for r in CONFIG['residences']
    ]
    return jsonify(data)

@remote_bp.route('/api/residences/<res_id>/relays')
@login_required
def api_get_relays(res_id):
    if current_user.role != 'operator':
        return jsonify(error='Forbidden'), 403

    # Busca la residencia en tu CONFIG
    res_cfg = next((r for r in CONFIG['residences'] if r['id'] == res_id), None)
    if not res_cfg:
        return jsonify(error='Not found'), 404

    # Instancia pasando TODO el dict
    device = RelayDevice(res_cfg)

    # Pide estados (sin cambiar nada)
    states = device.set_and_get_states(None, None)

    # Mezcla nombre y estado
    output = []
    for rl in res_cfg['relays']:
        rid = rl['id']
        output.append({
            'relay_id': rid,
            'name':     rl['name'],
            'state':    states.get(rid, 'Off')
        })

    return jsonify(output)
