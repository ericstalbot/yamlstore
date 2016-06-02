from flask import session, request, redirect, url_for, render_template, \
    json, flash

from flask_user import login_required, current_user

from yamlstore import app
from yamlstore.models import YamlDocument, EditDocumentForm
from yamlstore.yaml_handling import InvalidYaml, process_yaml


@app.route('/users/<int:user_id>/docs')
def view_user_documents():
    return current_user.username
    #if logged in, show list of document titles
    #else, see other to log in page


@app.route('/new', methods=['POST'])
@login_required
def new_yaml_doc():
    doc = YamlDocument(current_user.ID)
    db.session.add(doc)
    db.session.commit()
    redirect(url_for('edit_yaml_doc', doc_id=doc.id))


@app.route('/docs/<int:doc_id>')
def view_yaml_doc(doc_id):
    doc = YamlDocument.query.get_or_404(doc_id) 
    
    belongs_to_current_user = doc.user == current_user
    
    return render_template('view_doc.html', doc=doc, belongs_to_current_user=belongs_to_current_user)
    
    

@app.route('/docs/<int:doc_id>/json')
def get_json(doc_id):
    doc = YamlDocument.query.get_or_404(doc_id) 
    return doc.json, {'Content-type':'application/json'}



    
@app.route('/docs/<int:doc_id>/edit', methods=['GET', 'PUT'])
@login_required    
def edit_yaml_doc(doc_id):
    
    doc = YamlDocument.query.get_or_404(doc_id)
    
    if doc.user != current_user:
        return 'to do: better response here'
    
    form = EditDocumentForm(request.form, doc)
    
    if (form.method == 'PUT') and (form.validate()):
        
        try:
            json_string = process_yaml(form.document.data)
        except InvalidYaml as e:
            form.errors['document'].append(e.msg) # can i do this?
            valid = False
        else:
            valid = True
            
    if valid:
        
        form.populate_obj(doc)
        doc.json = json_string
        db.session.commit()
        flash('yaml document saved', 'alert-success')
        return redirect(url_for(view_yaml_doc, doc_id=doc_id))
                
    
    return render_template('edit_doc.html', form=form)