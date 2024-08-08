import bpy

def nodesVertexPBR(objekti):
    obj = bpy.context.active_object
    has_color = False

    # Ensure the object is a mesh
    if obj.type == 'MESH':
        # Check if there is vertex color data
        if len(obj.data.vertex_colors) > 0:
            print("Vertex color data exists.")
            for color_layer in obj.data.vertex_colors:
                has_color = True

    Prin_mat = None
    Node_Tree = objekti.active_material.node_tree
    for node in Node_Tree.nodes:
        if node.type == "BSDF_PRINCIPLED":
            Prin_mat = node
            break
    if Prin_mat != None and has_color:        
        col_attribute = Node_Tree.nodes.new(type="ShaderNodeVertexColor")
        col_attribute.layer_name = "vertex_color"
        col_attribute.location = -400, 200
        mix_rgb = Node_Tree.nodes.new(type="ShaderNodeMixRGB")
        mix_rgb.location = -200, 450
        rgb = Node_Tree.nodes.new(type="ShaderNodeRGB")
        rgb.location = -400, 400

        col_attribute_gm = Node_Tree.nodes.new(type="ShaderNodeVertexColor")
        col_attribute_gm.layer_name = "vertex_gloss_metall"
        col_attribute_gm.location = -800, 50

        gamma = Node_Tree.nodes.new(type="ShaderNodeGamma")
        gamma.inputs['Gamma'].default_value = 0.4545
        gamma.location = -600, 50

        separate = Node_Tree.nodes.new(type="ShaderNodeSeparateXYZ")
        separate.location = -400, 50

        mapper = Node_Tree.nodes.new(type="ShaderNodeMapRange")
        mapper.inputs['To Min'].default_value = 1
        mapper.inputs['To Max'].default_value = 0
        mapper.location = -200, 0   

        Node_Tree.links.new(col_attribute_gm.outputs['Color'], gamma.inputs['Color'])
        Node_Tree.links.new(gamma.outputs['Color'], separate.inputs['Vector'])
        Node_Tree.links.new(separate.outputs['Z'], mapper.inputs['Value'])
        Node_Tree.links.new(mapper.outputs['Result'], Prin_mat.inputs['Roughness'])
        Node_Tree.links.new(separate.outputs['Y'], Prin_mat.inputs['Metallic'])

        Node_Tree.links.new(col_attribute.outputs['Color'], mix_rgb.inputs['Color2'])
        Node_Tree.links.new(col_attribute.outputs['Alpha'], mix_rgb.inputs['Fac'])
        Node_Tree.links.new(rgb.outputs['Color'], mix_rgb.inputs['Color1'])
        Node_Tree.links.new(mix_rgb.outputs['Color'], Prin_mat.inputs['Base Color'])