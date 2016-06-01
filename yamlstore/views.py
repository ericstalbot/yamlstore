from flask import session, request, redirect, url_for, render_template

from flask_user import login_required, current_user

from yamlstore import app
from yamlstore.models import YamlDocument, EditDocumentForm
from yamlstore.yaml_handling import InvalidYaml, process_yaml


@app.route('/')
@login_required
def view_documents():
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
    
@app.route('/edit/<int:doc_id>', methods=['GET', 'PUT'])
@login_required    
def edit_yaml_doc(doc_id):
    
    doc = YamlDocument.query.get(doc_id)
    
    if doc.user != current_user:
        return 'to do: better response here'
    
    form = EditDocumentForm(request.form, doc)
    
    if (form.method == 'PUT') and (form.validate()):
        
        try:
            json_string = process_yaml(form.document.data)
        except InvalidYaml as e:
            form.errors['document'].append(e.msg)
            valid = False
        else:
            valid = True
            
    if valid:
        
        form.populate_obj(doc)
        doc.json = json_string
        db.session.commit()
        return redirect(url_for(view_yaml_doc, doc_id=doc_id))
                
    
    return render_template('edit_doc.html', form=form)
    
    
    



    

    
    
