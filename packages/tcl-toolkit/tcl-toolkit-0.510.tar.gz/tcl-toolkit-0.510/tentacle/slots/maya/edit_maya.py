# !/usr/bin/python
# coding=utf-8
from slots.maya import *
from slots.edit import Edit



class Edit_maya(Edit, Slots_maya):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		dh = self.sb.edit.draggable_header
		items = ['Cleanup', 'Transfer: Attribute Values', 'Transfer: Shading Sets']
		dh.ctxMenu.cmb000.addItems_(items, 'Maya Editors')

		tb000 = self.sb.edit.tb000
		tb000.ctxMenu.add('QCheckBox', setText='All Geometry', setObjectName='chk005', setToolTip='Clean All scene geometry.')
		tb000.ctxMenu.add('QCheckBox', setText='Repair', setObjectName='chk004', setToolTip='Repair matching geometry. Else, select only.') #add(self.sb.CheckBox, setText='Select Only', setObjectName='chk004', setTristate=True, setCheckState_=2, setToolTip='Select and/or Repair matching geometry. <br>0: Repair Only<br>1: Repair and Select<br>2: Select Only')
		tb000.ctxMenu.add('QCheckBox', setText='Merge vertices', setObjectName='chk024', setChecked=True, setToolTip='Merge overlapping vertices on the object(s) before executing the clean command.')
		tb000.ctxMenu.add('QCheckBox', setText='N-Gons', setObjectName='chk002', setChecked=True, setToolTip='Find N-gons.')
		tb000.ctxMenu.add('QCheckBox', setText='Non-Manifold Geometry', setObjectName='chk017', setChecked=True, setToolTip='Check for nonmanifold polys.')
		tb000.ctxMenu.add('QCheckBox', setText='Non-Manifold Vertex', setObjectName='chk021', setToolTip='A connected vertex of non-manifold geometry where the faces share a single vertex.')
		tb000.ctxMenu.add('QCheckBox', setText='Quads', setObjectName='chk010', setToolTip='Check for quad sided polys.')
		tb000.ctxMenu.add('QCheckBox', setText='Concave', setObjectName='chk011', setToolTip='Check for concave polys.')
		tb000.ctxMenu.add('QCheckBox', setText='Non-Planar', setObjectName='chk003', setToolTip='Check for non-planar polys.')
		tb000.ctxMenu.add('QCheckBox', setText='Holed', setObjectName='chk012', setToolTip='Check for holed polys.')
		tb000.ctxMenu.add('QCheckBox', setText='Lamina', setObjectName='chk018', setChecked=True, setToolTip='Check for lamina polys.')
		tb000.ctxMenu.add('QCheckBox', setText='Shared UV\'s', setObjectName='chk016', setToolTip='Unshare uvs that are shared across vertices.')
		# tb000.ctxMenu.add('QCheckBox', setText='Invalid Components', setObjectName='chk019', setToolTip='Check for invalid components.')
		tb000.ctxMenu.add('QCheckBox', setText='Zero Face Area', setObjectName='chk013', setChecked=True, setToolTip='Check for 0 area faces.')
		tb000.ctxMenu.add('QDoubleSpinBox', setPrefix='Face Area Tolerance:   ', setObjectName='s006', setMinMax_='0.0-10 step.000010', setValue=0.000010, setToolTip='Tolerance for face areas.')
		tb000.ctxMenu.add('QCheckBox', setText='Zero Length Edges', setObjectName='chk014', setChecked=True, setToolTip='Check for 0 length edges.')
		tb000.ctxMenu.add('QDoubleSpinBox', setPrefix='Edge Length Tolerance: ', setObjectName='s007', setMinMax_='0.0-10 step.000010', setValue=0.000010, setToolTip='Tolerance for edge length.')
		tb000.ctxMenu.add('QCheckBox', setText='Zero UV Face Area', setObjectName='chk015', setToolTip='Check for 0 uv face area.')
		tb000.ctxMenu.add('QDoubleSpinBox', setPrefix='UV Face Area Tolerance:', setObjectName='s008', setDisabled=True, setMinMax_='0.0-10 step.000010', setValue=0.000010, setToolTip='Tolerance for uv face areas.')
		tb000.ctxMenu.add('QCheckBox', setText='Overlapping Faces', setObjectName='chk025', setToolTip='Find any overlapping duplicate faces. (can be very slow on dense objects)')
		tb000.ctxMenu.add('QCheckBox', setText='Overlapping Duplicate Objects', setObjectName='chk022', setToolTip='Find any duplicate overlapping geometry at the object level.')
		tb000.ctxMenu.add('QCheckBox', setText='Omit Selected Objects', setObjectName='chk023', setDisabled=True, setToolTip='Overlapping Duplicate Objects: Search for duplicates of any selected objects while omitting the initially selected objects.')
		tb000.ctxMenu.chk013.toggled.connect(lambda state: tb000.ctxMenu.s006.setEnabled(True if state else False))
		tb000.ctxMenu.chk014.toggled.connect(lambda state: tb000.ctxMenu.s007.setEnabled(True if state else False))
		tb000.ctxMenu.chk015.toggled.connect(lambda state: tb000.ctxMenu.s008.setEnabled(True if state else False))
		tb000.ctxMenu.chk022.stateChanged.connect(lambda state: self.sb.toggleWidgets(tb000.ctxMenu, setDisabled='chk002-3,chk005,chk010-21,chk024,s006-8', setEnabled='chk023') if state 
														else self.sb.toggleWidgets(tb000.ctxMenu, setEnabled='chk002-3,chk005,chk010-21,s006-8', setDisabled='chk023')) #disable non-relevant options.
		#sync widgets
		self.sb.setSyncConnections(tb000.ctxMenu.chk004, self.sb.edit_submenu.chk004, attributes='setChecked')
		self.sb.setSyncConnections(tb000.ctxMenu.chk010, self.sb.edit_submenu.chk010, attributes='setChecked')


	def cmb000(self, index=-1):
		'''Editors
		'''
		cmb = self.sb.edit.draggable_header.ctxMenu.cmb000

		if index>0:
			text = cmb.items[index]
			if text=='Cleanup':
				pm.mel.CleanupPolygonOptions()
			elif text=='Transfer: Attribute Values':
				pm.mel.TransferAttributeValuesOptions()
				# mel.eval('performTransferAttributes 1;') #Transfer Attributes Options
			elif text=='Transfer: Shading Sets':
				pm.mel.performTransferShadingSets(1)
			cmb.setCurrentIndex(0)


	@Slots_maya.attr
	def cmb001(self, index=-1):
		'''Object History Attributes
		'''
		cmb = self.sb.edit.cmb001

		try:
			items = list(set([n.name() for n in pm.listHistory(pm.ls(sl=1, objectsOnly=1), pruneDagObjects=1)])) #levels=1, interestLevel=2, 
		except RuntimeError as error:
			items = ['No selection.']
		cmb.addItems_(items, 'History')

		cmb.setCurrentIndex(0)
		if index>0:
			if cmb.items[index]!='No selection.':
				return pm.ls(cmb.items[index])


	def tb000(self, state=None):
		'''Mesh Cleanup
		'''
		tb = self.sb.edit.tb000

		allMeshes = int(tb.ctxMenu.chk005.isChecked()) #[0] All selectable meshes
		repair = tb.ctxMenu.chk004.isChecked() #repair or select only
		quads = int(tb.ctxMenu.chk010.isChecked()) #[3] check for quads polys
		mergeVertices = tb.ctxMenu.chk024.isChecked()
		nsided = int(tb.ctxMenu.chk002.isChecked()) #[4] check for n-sided polys
		concave = int(tb.ctxMenu.chk011.isChecked()) #[5] check for concave polys
		holed = int(tb.ctxMenu.chk012.isChecked()) #[6] check for holed polys
		nonplanar = int(tb.ctxMenu.chk003.isChecked()) #[7] check for non-planar polys
		zeroGeom = int(tb.ctxMenu.chk013.isChecked()) #[8] check for 0 area faces
		zeroGeomTol = tb.ctxMenu.s006.value() #[9] tolerance for face areas
		zeroEdge = int(tb.ctxMenu.chk014.isChecked()) #[10] check for 0 length edges
		zeroEdgeTol = tb.ctxMenu.s007.value() #[11] tolerance for edge length
		zeroMap = int(tb.ctxMenu.chk015.isChecked()) #[12] check for 0 uv face area
		zeroMapTol = tb.ctxMenu.s008.value() #[13] tolerance for uv face areas
		sharedUVs = int(tb.ctxMenu.chk016.isChecked()) #[14] Unshare uvs that are shared across vertices
		nonmanifold = int(tb.ctxMenu.chk017.isChecked()) #[15] check for nonmanifold polys
		lamina = -int(tb.ctxMenu.chk018.isChecked()) #[16] check for lamina polys [default -1]
		splitNonManifoldVertex = tb.ctxMenu.chk021.isChecked()
		invalidComponents = 0 #int(tb.ctxMenu.chk019.isChecked()) #[17] a guess what this arg does. not checked. default is 0.
		overlappingFaces = tb.ctxMenu.chk025.isChecked()
		overlappingDuplicateObjects = tb.ctxMenu.chk022.isChecked() #find overlapping geometry at object level.
		omitSelectedObjects = tb.ctxMenu.chk023.isChecked() #Search for duplicates of any selected objects while omitting the initially selected objects.

		objects = pm.ls(sl=1, transforms=1)

		if overlappingDuplicateObjects:
			duplicates = self.getOverlappingDuplicateObjects(omitInitialObjects=omitSelectedObjects, select=True, verbose=True)
			self.messageBox('Found {} duplicate overlapping objects.'.format(len(duplicates)), messageType='Result')
			pm.delete(duplicates) if repair else pm.select(duplicates)
			return

		if mergeVertices:
			[pm.polyMergeVertex(obj.verts, distance=0.0001) for obj in objects] #merge vertices on each object.

		if overlappingFaces:
			duplicates = self.getOverlappingFaces(objects)
			self.messageBox('Found {} duplicate overlapping faces.'.format(len(duplicates)), messageType='Result')
			pm.delete(duplicates) if repair else pm.select(duplicates, add=1)

		self.cleanGeometry(objects, allMeshes=allMeshes, repair=repair, quads=quads, nsided=nsided, concave=concave, holed=holed, nonplanar=nonplanar, 
			zeroGeom=zeroGeom, zeroGeomTol=zeroGeomTol, zeroEdge=zeroEdge, zeroEdgeTol=zeroEdgeTol, zeroMap=zeroMap, zeroMapTol=zeroMapTol, 
			sharedUVs=sharedUVs, nonmanifold=nonmanifold, invalidComponents=invalidComponents, splitNonManifoldVertex=splitNonManifoldVertex)


	def tb001(self, state=None):
		'''Delete History
		'''
		tb = self.sb.edit.tb001

		all_ = tb.ctxMenu.chk018.isChecked()
		unusedNodes = tb.ctxMenu.chk019.isChecked()
		deformers = tb.ctxMenu.chk020.isChecked()
		optimize = tb.ctxMenu.chk030.isChecked()

		objects = pm.ls(selection=1, objectsOnly=1) if not all_ else pm.ls(typ="mesh")

		if optimize:
			pm.mel.OptimizeScene()

		try: #delete history
			if all_:
				pm.delete(objects, constructionHistory=1)
			else:
				pm.bakePartialHistory(objects, prePostDeformers=1)
		except:
			pass
		if unusedNodes:
			pm.mel.MLdeleteUnused() #pm.mel.hyperShadePanelMenuCommand('hyperShadePanel1', 'deleteUnusedNodes')

		#display viewPort messages
		if all_:
			if deformers:
				self.viewPortMessage("delete <hl>all</hl> history.")
			else:
				self.viewPortMessage("delete <hl>all non-deformer</hl> history.")
		else:
			if deformers:
				self.viewPortMessage("delete history on "+str(objects))
			else:
				self.viewPortMessage("delete <hl>non-deformer</hl> history on "+str(objects))


	def tb002(self, state=None):
		'''Delete
		'''
		tb = self.sb.edit.tb002

		deleteRing = tb.ctxMenu.chk000.isChecked()
		deleteLoop = tb.ctxMenu.chk001.isChecked()

		# selectionMask = pm.selectMode (query=True, component=True)
		maskVertex = pm.selectType (query=True, vertex=True)
		maskEdge = pm.selectType (query=True, edge=True)
		maskFacet = pm.selectType (query=True, facet=True)

		objects = pm.ls(sl=1, objectsOnly=1)
		for obj in objects:
			if pm.objectType(obj, isType='joint'):
				pm.removeJoint(obj) #remove joints

			elif pm.objectType(obj, isType='mesh'): 
				if maskEdge:
					selection = pm.ls(obj, sl=1, flatten=1)
					if deleteRing:
						pm.polyDelEdge(self.getEdgePath(selection, 'edgeRing'), cleanVertices=True) # pm.polySelect(edges, edgeRing=True) #select the edge ring.
					if deleteLoop:
						pm.polyDelEdge(self.getEdgePath(selection, 'edgeLoop'), cleanVertices=True) # pm.polySelect(edges, edgeLoop=True) #select the edge loop.
					else:
						pm.polyDelEdge(selection, cleanVertices=True) #delete edges

				elif maskVertex:
					pm.polyDelVertex() #try delete vertices
					if pm.ls(sl=1)==objects: #if nothing was deleted:
						mel.eval('polySelectSp -loop;') #convert selection to edge loop
						pm.polyDelEdge(cleanVertices=True) #delete edges

				else: #all([selectionMask==1, maskFacet==1]):
					pm.delete(obj) #delete faces\mesh objects


	def tb003(self, state=None):
		'''Delete Along Axis
		'''
		tb = self.sb.edit.tb003

		axis = self.sb.getAxisFromCheckBoxes('chk006-9', tb.ctxMenu)

		pm.undoInfo(openChunk=1)
		objects = pm.ls(sl=1, objectsOnly=1)

		for obj in objects:
			self.deleteAlongAxis(obj, axis)
		pm.undoInfo(closeChunk=1)


	@Slots_maya.undo
	def tb004(self, state=None):
		'''Delete Along Axis
		'''
		tb = self.sb.edit.tb004

		allNodes = tb.ctxMenu.chk026.isChecked()
		unlock = tb.ctxMenu.chk027.isChecked()

		# pm.undoInfo(openChunk=1)
		nodes = pm.ls() if allNodes else pm.ls(selection=1)
		for node in nodes:
			pm.lockNode(node, lock=not unlock)
		# pm.undoInfo(closeChunk=1)


	@Slots.hideMain
	def b001(self):
		'''Object History Attributes: get most recent node
		'''
		cmb = self.sb.edit.cmb001
		self.cmb001() #refresh the contents of the combobox.

		items = pm.ls(cmb.items[-1])
		if items:
			self.setAttributeWindow(items, checkableLabel=True)
		else:
			self.messageBox('Found no items to list the history for.')
			return


	def b021(self):
		'''Tranfer Maps
		'''
		pm.mel.performSurfaceSampling(1)


	def b022(self):
		'''Transfer Vertex Order
		'''
		pm.mel.TransferVertexOrder()


	def b023(self):
		'''Transfer Attribute Values
		'''
		pm.mel.TransferAttributeValues()


	def b027(self):
		'''Shading Sets
		'''
		pm.mel.performTransferShadingSets(0)


	def cleanGeometry(self, objects, allMeshes=False, repair=False, quads=False, nsided=False, concave=False, holed=False, nonplanar=False, 
					zeroGeom=False, zeroGeomTol=0.000010, zeroEdge=False, zeroEdgeTol=0.000010, zeroMap=False, zeroMapTol=0.000010, 
					sharedUVs=False, nonmanifold=False, lamina=False, invalidComponents=False, splitNonManifoldVertex=False, historyOn=True):
		'''Select or remove unwanted geometry from a polygon mesh.

		:Parameters:
			objects (str)(obj)(list) = The polygon objects to clean.
			allMeshes (bool) = Clean all geomtry in the scene instead of only the current selection.
			repair (bool) = Attempt to repair instead of just selecting geometry.
		'''
		arg_list = '"{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}","{9}","{10}","{11}","{12}","{13}","{14}","{15}","{16}","{17}"'.format(
				allMeshes, 1 if repair else 2, historyOn, quads, nsided, concave, holed, nonplanar, zeroGeom, zeroGeomTol, 
				zeroEdge, zeroEdgeTol, zeroMap, zeroMapTol, sharedUVs, nonmanifold, lamina, invalidComponents)
		command = 'polyCleanupArgList 4 {'+arg_list+'}' # command = 'polyCleanup '+arg_list #(not used because of arg count error, also the quotes in the arg list would need to be removed). 

		if splitNonManifoldVertex: #Split Non-Manifold Vertex
			nonManifoldVerts = self.findNonManifoldVertex(objects, select=2) #Select: 0=off, 1=on, 2=on while keeping any existing vertex selections. (default: 1)
			if repair:
				for vertex in nonManifoldVerts:
					self.splitNonManifoldVertex(vertex, select=True) #select(bool): Select the vertex after the operation. (default: True)

		pm.select(objects)
		mel.eval(command); #print (command)


	def getOverlappingDuplicateObjects(self, objects=[], omitInitialObjects=False, select=False, verbose=False):
		'''Find any duplicate overlapping geometry at the object level.

		:Parameters:
			objects (list) = A list of objects to find duplicate overlapping geometry for. Default is selected objects, or all if nothing is selected.
			omitInitialObjects (bool) = Search only for duplicates of the given objects (or any selected objects if None given), and omit them from the return results.
			select (bool) = Select any found duplicate objects.
			verbose (bool) = Print each found object to console.

		:Return:
			(set)

		ex call: duplicates = getOverlappingDuplicateObjects(omitInitialObjects=True, select=True, verbose=True)
		'''
		scene_objs = pm.ls(transforms=1, geometry=1) #get all scene geometry

		#attach a unique identifier consisting each objects polyEvaluate attributes, and it's bounding box center point in world space.
		scene_objs = {i:str(pm.objectCenter(i))+str(pm.polyEvaluate(i)) for i in scene_objs if not Slots_maya.isGroup(i)}
		selected_objs = pm.ls(scene_objs.keys(), sl=1) if not objects else objects

		objs_inverted={} #invert the dict, combining objects with like identifiers.
		for k, v in scene_objs.items():
			objs_inverted[v] = objs_inverted.get(v, []) + [k]

		duplicates=set()
		for k, v in objs_inverted.items():
			if len(v)>1:
				if selected_objs: #limit scope to only selected objects.
					if set(selected_objs) & set(v): #if any selected objects in found duplicates:
						if omitInitialObjects:
							[duplicates.add(i) for i in v if i not in selected_objs] #add any duplicated of that object, omitting the selected object.
						else:
							[duplicates.add(i) for i in v[1:]] #add all but the first object to the set of duplicates.
				else:
					[duplicates.add(i) for i in v[1:]] #add all but the first object to the set of duplicates.

		if verbose:
			for i in duplicates:
				print (' # Found: overlapping duplicate object: {} #'.format(i))
		print (' # {} overlapping duplicate objects found. #'.format(len(duplicates)))

		if select:
			pm.select(duplicates)

		return duplicates


	def deleteAlongAxis(self, obj, axis):
		'''Delete components of the given mesh object along the specified axis.

		:Parameters:
			obj (obj) = Mesh object.
			axis (str) = Axis to delete on. ie. '-x' Components belonging to the mesh object given in the 'obj' arg, that fall on this axis, will be deleted. 
		'''
		for node in [n for n in pm.listRelatives(obj, allDescendents=1) if pm.objectType(n, isType='mesh')]: #get any mesh type child nodes of obj.
			faces = self.getAllFacesOnAxis(node, axis)
			if len(faces)==pm.polyEvaluate(node, face=1): #if all faces fall on the specified axis.
				pm.delete(node) #delete entire node
			else:
				pm.delete(faces) #else, delete any individual faces.

		Slots_maya.viewPortMessage("Delete faces on <hl>"+axis.upper()+"</hl>.")


	def getAllFacesOnAxis(self, obj, axis="-x", localspace=False):
		'''Get all faces on a specified axis.

		:Parameters:
			obj (str)(obj) = The name of the geometry.
			axis (str) = The representing axis. case insensitive. (valid: 'x', '-x', 'y', '-y', 'z', '-z')
			localspace (bool) = Specify world or local space.

		ex call: self.getAllFacesOnAxis('polyObject', 'y')
		'''
		axis = axis.lower() #assure case.

		i=0 #'x'
		if any ([axis=="y",axis=="-y"]):
			i=1
		if any ([axis=="z",axis=="-z"]):
			i=2

		objName = pm.ls(obj)[0].name()

		if axis.startswith('-'): #any([axis=="-x", axis=="-y", axis=="-z"]):
			return list(face for face in pm.filterExpand(objName+'.f[*]', sm=34) if pm.exactWorldBoundingBox(face)[i] < -0.00001)
		else:
			return list(face for face in pm.filterExpand(objName+'.f[*]', sm=34) if pm.exactWorldBoundingBox(face)[i] > -0.00001)


	@Slots_maya.undo
	def findNonManifoldVertex(self, objects, select=1):
		'''Locate a connected vertex of non-manifold geometry where the faces share a single vertex.

		:Parameters:
			objects (str)(obj) = A polygon mesh, or a list of meshes.
			select (int) = Select any found non-manifold vertices. 0=off, 1=on, 2=on while keeping any existing vertex selections. (default: 1)

		:Return:
			(list) any found non-manifold verts.
		'''
		# pm.undoInfo(openChunk=True)
		nonManifoldVerts=set()

		vertices = self.getComponents(objects, 'vertices')
		for vertex in vertices:

			connected_faces = pm.polyListComponentConversion(vertex, fromVertex=1, toFace=1) #pm.mel.PolySelectConvert(1) #convert to faces
			connected_faces_flat = pm.ls(connected_faces, flatten=1) #selectedFaces = pm.ls(sl=1, flatten=1)

			#get a list of the edges of each face that is connected to the original vertex.
			edges_sorted_by_face=[]
			for face in connected_faces_flat:

				connected_edges = pm.polyListComponentConversion(face, fromFace=1, toEdge=1) #pm.mel.PolySelectConvert(1) #convert to faces
				connected_edges_flat = [str(i) for i in pm.ls(connected_edges, flatten=1)] #selectedFaces = pm.ls(sl=1, flatten=1)
				edges_sorted_by_face.append(connected_edges_flat)

			out=[] #1) take first set A from list. 2) for each other set B in the list do if B has common element(s) with A join B into A; remove B from list. 3) repeat 2. until no more overlap with A. 4) put A into outpup. 5) repeat 1. with rest of list.
			while len(edges_sorted_by_face)>0:
				first, rest = edges_sorted_by_face[0], edges_sorted_by_face[1:] #first list, all other lists, of the list of lists.
				first = set(first)

				lf = -1
				while len(first)>lf:
					lf = len(first)

					rest2=[]
					for r in rest:
						if len(first.intersection(set(r)))>0:
							first |= set(r)
						else:
							rest2.append(r)     
					rest = rest2

				out.append(first)
				edges_sorted_by_face = rest

			if len(out)>1:
				nonManifoldVerts.add(vertex)
		# pm.undoInfo(closeChunk=True)

		if select==2:
			pm.select(nonManifoldVerts, add=1)
		elif select==1:
			pm.select(nonManifoldVerts)

		return nonManifoldVerts


	@Slots_maya.undo
	def splitNonManifoldVertex(self, vertex, select=True):
		'''Separate a connected vertex of non-manifold geometry where the faces share a single vertex.

		:Parameters:
			vertex (str)(obj) = A single polygon vertex.
			select (bool) = Select the vertex after the operation. (default is True)
		'''
		# pm.undoInfo(openChunk=True)
		connected_faces = pm.polyListComponentConversion(vertex, fromVertex=1, toFace=1) #pm.mel.PolySelectConvert(1) #convert to faces
		connected_faces_flat = pm.ls(connected_faces, flatten=1) #selectedFaces = pm.ls(sl=1, flatten=1)

		pm.polySplitVertex(vertex)

		#get a list for the vertices of each face that is connected to the original vertex.
		verts_sorted_by_face=[]
		for face in connected_faces_flat:

			connected_verts = pm.polyListComponentConversion(face, fromFace=1, toVertex=1) #pm.mel.PolySelectConvert(1) #convert to faces
			connected_verts_flat = [str(i) for i in pm.ls(connected_verts, flatten=1)] #selectedFaces = pm.ls(sl=1, flatten=1)
			verts_sorted_by_face.append(connected_verts_flat)

		out=[] #1) take first set A from list. 2) for each other set B in the list do if B has common element(s) with A join B into A; remove B from list. 3) repeat 2. until no more overlap with A. 4) put A into outpup. 5) repeat 1. with rest of list.
		while len(verts_sorted_by_face)>0:
			first, rest = verts_sorted_by_face[0], verts_sorted_by_face[1:] #first, *rest = verts_sorted_by_face
			first = set(first)

			lf = -1
			while len(first)>lf:
				lf = len(first)

				rest2=[]
				for r in rest:
					if len(first.intersection(set(r)))>0:
						first |= set(r)
					else:
						rest2.append(r)     
				rest = rest2

			out.append(first)
			verts_sorted_by_face = rest


		for vertex_set in out:
			pm.polyMergeVertex(vertex_set, distance=0.001)

		pm.select(vertex_set, deselect=1) #deselect the vertices that were selected during the polyMergeVertex operation.
		if select:
			pm.select(vertex, add=1)
		# pm.undoInfo(closeChunk=True)


	def getNGons(self, obj, repair=False):
		'''Get any N-Gons from the given object.
		'''
		if nGons: #N-Sided Faces
			if repair: #Maya Bonus Tools: Convert N-Sided Faces To Quads
				try:
					mel.eval('bt_polyNSidedToQuad;')
				except:
					print('Maya Bonus Tools: Convert N-Sided Faces To Quads not found. (bt_polyNSidedToQuad;)')

			else: #Find And Select N-Gons
				pm.select(obj)
				#Change to Component mode to retain object highlighting for better visibility
				pm.changeSelectMode(component=1)
				#Change to Face Component Mode
				pm.selectType(smp=0, sme=1, smf=0, smu=0, pv=0, pe=1, pf=0, puv=0)
				#Select Object/s and Run Script to highlight N-Gons
				pm.polySelectConstraint(mode=3, type=0x0008, size=3)
				pm.polySelectConstraint(disable=1)
				#Populate an in-view message
				nGons = pm.polyEvaluate(faceComponent=1)
				Slots_maya.viewPortMessage("<hl>"+str(nGons[0])+"</hl> N-Gon(s) found.")


	def getOverlappingVertices(self, objects, threshold=0.0003):
		'''
		'''
		import maya.OpenMaya as om

		points_list = om.MPointArray()
		mfn_mesh.getPoints(points_list, om.MSpace.kWorld)

		result=[]
		for i in range(points_list.length()):
			for ii in range(points_list.length()):
				if i==ii:
					continue

				dist = points_list[i].distanceTo(points_list[ii])
				if dist < threshold:
					if i not in result:
						result.append(i)

					if ii not in result:
						result.append(ii)

		return result


	def getOverlappingFaces(self, objects):
		'''Get any duplicate overlapping faces of the given objects.

		::Parameters:
			objects (str)(obj)(list) = Faces or polygon objects.

		:Return:
			(list) duplicate overlapping faces.

		ex. call: pm.select(getOverlappingFaces(selection))
		'''
		if not pm.nodeType(objects[0])=='mesh': #if the objects are not faces.
			duplicates = [self.getOverlappingFaces(obj.faces) for obj in pm.ls(objects, objectsOnly=1)]
			return [i for sublist in duplicates for i in sublist] #flatten list.

		duplicates=[]

		face = pm.ls(objects)[0]
		face_vtx_positions = [v.getPosition() for v in pm.ls(pm.polyListComponentConversion(face, toVertex=1), flatten=1)]

		otherFaces = [f for f in objects if f!=face]
		for otherFace in otherFaces:
			otherFace_vtx_positions = [v.getPosition() for v in pm.ls(pm.polyListComponentConversion(otherFace, toVertex=1), flatten=1)]

			if face_vtx_positions==otherFace_vtx_positions: #duplicate found.
				duplicates.append(otherFace)
				otherFaces.remove(otherFace)

		if otherFaces:
			duplicates+=self.getOverlappingFaces(otherFaces) #after adding any found duplicates, call again with any remaining faces.

		return duplicates


	def getSimilarMesh(self, obj, tol=0.0, includeOrig=False, **kwargs):
		'''Find similar geometry objects using the polyEvaluate command.
		Default behaviour is to compare all flags.

		:parameters:
			obj (str)(obj)(list) = The object to find similar for.
			tol (float) = The allowed difference in any of the given polyEvalute flag results (that return an int, float (or list of the int or float) value(s)).
			includeOrig (bool) = Include the original given obj with the return results.
			kwargs (bool) = Any keyword argument 'polyEvaluate' takes. Used to filter the results.
				ex: vertex, edge, face, uvcoord, triangle, shell, boundingBox, boundingBox2d, 
				vertexComponent, boundingBoxComponent, boundingBoxComponent2d, area, worldArea
		:return:
			(list) Similar objects (excluding the given obj)

		ex. call: getSimilarMesh(selection, vertex=1, area=1)
		'''
		lst = lambda x: list(x) if isinstance(x, (list, tuple, set)) else list(x.values()) if isinstance(x, dict) else [x] #assure the returned result from polyEvaluate is a list of values.

		obj, *other = pm.ls(obj, long=True, transforms=True)
		objProps = lst(pm.polyEvaluate(obj, **kwargs))

		otherSceneMeshes = set(pm.filterExpand(pm.ls(long=True, typ='transform'), selectionMask=12)) #polygon selection mask.
		similar = pm.ls([m for m in otherSceneMeshes if Slots.areSimilar(objProps, lst(pm.polyEvaluate(m, **kwargs)), tol=tol) and m!=obj])
		return similar+[obj] if includeOrig else similar


	def getSimilarTopo(self, obj, includeOrig=False, **kwargs):
		'''Find similar geometry objects using the polyCompare command.
		Default behaviour is to compare all flags.

		:parameters:
			obj (str)(obj)(list) = The object to find similar for.
			includeOrig (bool) = Include the original given obj with the return results.
			kwargs (bool) = Any keyword argument 'polyCompare' takes. Used to filter the results.
				ex: vertices, edges, faceDesc, uvSets, uvSetIndices, colorSets, colorSetIndices, userNormals
		:return:
			(list) Similar objects (excluding the given obj)
		'''
		obj, *other = pm.filterExpand(pm.ls(obj, long=True, tr=True), selectionMask=12) #polygon selection mask.

		otherSceneMeshes = set(pm.filterExpand(pm.ls(long=True, typ='transform'), sm=12))
		similar = pm.ls([m for m in otherSceneMeshes if pm.polyCompare(obj, m, **kwargs)==0 and m!=obj]) #0:equal,Verts:1,Edges:2,Faces:4,UVSets:8,UVIndices:16,ColorSets:32,ColorIndices:64,UserNormals=128. So a return value of 3 indicates both vertices and edges are different.
		return similar+[obj] if includeOrig else similar








#module name
print (__name__)
# -----------------------------------------------
# Notes
# -----------------------------------------------
	# b008, b009, b011
