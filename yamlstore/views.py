from flask import session, request, redirect, url_for, render_template, \
    json, flash, jsonify

from flask_user import login_required, current_user

from yamlstore import app, db
from yamlstore.models import YamlDocument, EditDocumentForm, User
from yamlstore.yaml_handling import InvalidYaml, process_yaml

@app.route('/')
def index():
    return redirect(url_for('view_users'))


@app.route('/users')
def view_users():
    users = User.query.all()
    return render_template('view_users.html', users=users)
    

@app.route('/users/<int:user_id>/docs')
def view_user_docs(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('view_user_docs.html', user=user)
        
@app.route('/docs')
def view_yaml_docs():
    pass

@app.route('/docs/<int:doc_id>')
def view_yaml_doc(doc_id):
    doc = YamlDocument.query.get_or_404(doc_id) 
    
    belongs_to_current_user = doc.user == current_user
    
    return render_template('view_doc.html', doc=doc, belongs_to_current_user=belongs_to_current_user)


@app.route('/docs/<int:doc_id>/json')
def get_json(doc_id):
    
    doc = YamlDocument.query.get_or_404(doc_id)     
    return jsonify(json.loads(doc.json))

@app.route('/docs/new', methods=['POST'])
@login_required
def new_yaml_doc():
    doc = YamlDocument(current_user.id)
    db.session.add(doc)
    db.session.commit()
    return redirect(url_for('edit_yaml_doc', doc_id=doc.id))


@app.route('/docs/<int:doc_id>/edit', methods=['GET', 'POST'])
@login_required    
def edit_yaml_doc(doc_id):
    
    doc = YamlDocument.query.get_or_404(doc_id)
    
    if doc.user != current_user:
        return 'to do: better response here'
        
    form = EditDocumentForm(request.form, doc)
    
    if (request.method == 'POST') and form.validate():
        
        doc.title = form.title.data
        doc.document = form.document.data
        doc.json = form.document.json_string
        
        db.session.commit()
        
        flash('yaml document saved', 'alert-success')
        return redirect(url_for('view_yaml_doc', doc_id=doc_id))
                
    return render_template('edit_doc.html', form=form)