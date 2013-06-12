# tools/user/ide/owlxml.py
#
# Copyright 2012 Rice University.
#
# http://www.embeddedpython.org/
#
# This file is part of the Owl Embedded Python System and is provided under
# the MIT open-source license. See the LICENSE and COPYING files for details
# about your rights to use, modify, and distribute Owl.

import xml.etree.ElementTree, get, os, logging

logger = logging.getLogger(__name__)

CWD = os.getcwd()
logger.debug(CWD)

LAST_PATH = os.path.abspath(CWD+"/tmp/lastopened.xml")
PREF_PATH = os.path.abspath(CWD+"/tmp/preferences.xml")
REM_PATH = os.path.abspath(CWD+"/tmp/remembered.xml")

def save_project(project):

    if project:
        name = project.name
        current = project.current
        path = project.path
        files = project.files
    else:
        name = ''
        current = ''
        path = ''
        files = {}
    
    xmlstr = ''
    treebuilder = xml.etree.ElementTree.TreeBuilder()
    treebuilder.start('project',
                      {'name':name, 'current':current})
    is_empty = True
    for f in files:
        if f.startswith('Unsaved File'):
            continue
        is_empty = False
        if files[f]['is_open']:
            value = 'True'
        else:
            value = 'False'
        treebuilder.start('file',
                          {'name':f,
                           'page':str(files[f]['page']),
                           'is_open':value,
                           'path':str(files[f]['path'])})
        file_elem = treebuilder.end('file')
        xmlstr = xmlstr + '\n\t' + xml.etree.ElementTree.tostring(file_elem)

    element = treebuilder.end('project')
    elemstr = xml.etree.ElementTree.tostring(element)
    project_heading, close_bracket, subelems = elemstr.partition('>')

    if not path.endswith('.xml'):
        path = path + '.xml'

    pfile = open(path, 'w')
    pfile.write
    pfile.write(project_heading+'>')
    pfile.write(xmlstr)
    if not is_empty:
        pfile.write('\n</project>')
    pfile.close()

def get_project(projectpath):

    show_alert = True
    if projectpath == LAST_PATH:
        show_alert = False
    project_text = get.text_from_file(projectpath,show_alert)
    
    try:
        project_elem = xml.etree.ElementTree.fromstring(project_text)
    except:
        return
    name = project_elem.get('name')
    current = project_elem.get('current')
    file_elems = project_elem.findall('file')
    files = {}
    for f in file_elems:
        if f.get('is_open')in('True','true'):
            value = True
        else:
            value = False
        files[f.get('name')] = {'path':f.get('path'),
                                'page':int(f.get('page')),
                                'is_open':value}
    return name, current, files

def get_project_list(projectpath):
    project_text = get.text_from_file(projectpath)
    try:
        project_elem = xml.etree.ElementTree.fromstring(project_text)
    except:
        return None, None
    name = project_elem.get('name')
    file_elems = project_elem.findall('file')
    files = {}
    for f in file_elems:
        files[f.get('name')] = f.get('path')

    return name, files


def save_pref (pref, project, port):
    xmlstr = ''
    treebuilder = xml.etree.ElementTree.TreeBuilder()
    treebuilder.start('preferences',{})
    for p in pref:
        if pref[p]:
            value = 'True'
        else:
            value = 'False'
            
        if p == 'preference_openlastproject' and pref[p]:
            treebuilder.start('option', {'name':p, 'value':value, 'project':project})
        elif p == 'preference_autoconnect' and port:
            treebuilder.start('option', {'name':p, 'value':value, 'portname':port})
        else:
            treebuilder.start('option', {'name':p, 'value':value})
            
        prefelem = treebuilder.end('option')
        xmlstr = xmlstr + '\n\t' + xml.etree.ElementTree.tostring(prefelem)
    element = treebuilder.end('preferences') 
    elemstr = xml.etree.ElementTree.tostring(element)
    project_heading, close_bracket, subelems = elemstr.partition('>')
    

    pfile = open(PREF_PATH,'w')
    pfile.write(project_heading+'>')
    pfile.write(xmlstr)
    pfile.write('\n</preferences>')
    pfile.close()
    logger.debug('done pref')

def get_pref():
    
    pref_text = get.text_from_file(PREF_PATH,False)

    try:
        pref_elem = xml.etree.ElementTree.fromstring(pref_text)
    except:
        return

    preferences = {}
    project = None
    port = None
    
    options = pref_elem.findall('option')
    
    for opt in options:
        if opt.get('value')in('True','true'):
            value = True
        else:
            value = False
        preferences[opt.get('name')] = value
        if 'project' in opt.attrib and value:
            project = opt.attrib['project']
        if 'portname' in opt.attrib:
            port = opt.attrib['portname']

    return preferences, project, port


def save_recent(remembered):
    xmlstr = ''
    treebuilder = xml.etree.ElementTree.TreeBuilder()
    treebuilder.start('remembered',{})
    xmlstr = '<remembered>'
    
    treebuilder.start('recent_files',{})
    xmlstr += '\n\t<recent_files>'
    for filename in remembered.recent:
        treebuilder.start('file',
                          {'name':filename,
                           'path':remembered.recent[filename]})
        elem = treebuilder.end('file')
        xmlstr = xmlstr + '\n\t\t' + xml.etree.ElementTree.tostring(elem)
    treebuilder.end('recent_files')
    xmlstr += '\n\t</recent_files>'
    
    treebuilder.start('ports',{})
    xmlstr += '\n\t<ports>'
    for portname in remembered.ports:
        treebuilder.start('port', {'name':portname})
        elem = treebuilder.end('port')
        xmlstr = xmlstr + '\n\t\t' + xml.etree.ElementTree.tostring(elem)
    treebuilder.end('ports')
    xmlstr += '\n\t</ports>'
    
    treebuilder.start('dir', {'name':remembered.dir})
    elem = treebuilder.end('dir')
    xmlstr = xmlstr + '\n\t' + xml.etree.ElementTree.tostring(elem)

    treebuilder.start('proj_list', {})
    xmlstr += '\n\t<proj_list>'
    for projpath in remembered.projs:
        treebuilder.start('proj',{'path':projpath})
        elem = treebuilder.end('proj')
        xmlstr += '\n\t\t' + xml.etree.ElementTree.tostring(elem)
    treebuilder.end('proj_list')
    xmlstr += '\n\t</proj_list>'
    
    treebuilder.end('remembered')
    xmlstr += '\n</remembered>'

    rfile = open(REM_PATH, 'w')
    rfile.write(xmlstr)
    rfile.close()


def get_recent():

    r_text = get.text_from_file(REM_PATH,False)

    try:
        elem = xml.etree.ElementTree.fromstring(r_text)
    except:
        return

    recent = {}
    ports = set([])
    directory = None
    projs = []

    r_elem, p_elem, d_elem, proj_elem = list(elem)
    recent_files = r_elem.findall('file')
    for f in recent_files:
        recent[f.get('name')] = f.get('path')
    portelems = p_elem.findall('port')
    for p in portelems:
        ports.add(p.get('name'))

    directory = d_elem.get('name')

    projelems = proj_elem.findall('proj')
    for proj in projelems:
        projs.append(proj.get('path'))

    return recent, ports, directory, projs
