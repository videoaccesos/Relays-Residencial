from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from models import SessionLocal, Residence, Relay
admin_bp=Blueprint('admin',__name__,url_prefix='/config')
@admin_bp.before_request
def restrict():
    if not current_user.is_authenticated or current_user.role!='admin': return 'Acceso denegado',403
@admin_bp.route('/')
def panel(): return render_template('admin.html')
@admin_bp.route('/residences',methods=['GET','POST','DELETE','PUT'])
@login_required
def manage_residences():
    db=SessionLocal()
    if request.method=='GET':
        res=db.query(Residence).all(); return jsonify([{ 'id':r.id,'name':r.name,'type':r.type,'url_base':r.url_base} for r in res])
    data=request.get_json() or {}
    if request.method=='POST':
        r=Residence(id=data['id'],name=data['name'],type=data['type'],url_base=data['url_base'])
        db.add(r)
        for rr in data.get('relays',[]): db.add(Relay(residence_id=r.id,relay_id=rr['relay_id'],name=rr['name'],cmd_template=rr['cmd_template']))
    elif request.method=='PUT':
        r=db.query(Residence).get(data['id']); r.name=data['name'];r.url_base=data['url_base'];r.type=data['type']
    elif request.method=='DELETE':
        db.query(Residence).filter_by(id=request.args['id']).delete()
    db.commit(); db.close(); return jsonify({'status':'ok'})
