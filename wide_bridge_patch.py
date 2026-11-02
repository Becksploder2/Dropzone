from pathlib import Path
p = Path("DropZone_Godot4/scripts/main.gd")
s = p.read_text()
needle = ' install_branching_bridge()\n create_ui()'
if needle not in s:
    raise SystemExit("Could not locate existing bridge installation")
s = s.replace(needle, ' install_branching_bridge()\n restore_wide_bridge()\n create_ui()', 1)
s += '''

# Wide rectangular bridge inspired by the earlier set, while retaining 3/3/2/1 decisions.
# No pyramid silhouette: all four answer banks occupy the same full-width deck.
func restore_wide_bridge() -> void:
 var bridge_width=8.1
 var row_centers=[-4.7,-1.6,1.5,4.7]
 # Original eight broad crosswise deck strips. Their translucent finish keeps
 # the animated water visible underneath.
 for i in range(8):
  var segment=box_mesh(stage,Vector3(0,0.04,float(i)*1.55-5.43),Vector3(bridge_width,0.06,1.42),Color(0.05,0.24,0.45,0.30))
  var m=StandardMaterial3D.new()
  m.albedo_color=Color(0.02,0.24,0.42,0.26)
  m.transparency=BaseMaterial3D.TRANSPARENCY_ALPHA
  m.metallic=0.35
  m.roughness=0.25
  segment.material_override=m
 # Continuous rails and full-width row separators visually restore the old bridge.
 for edge_x in [-4.04,4.04]:
  neon(stage,Vector3(edge_x,0.20,0.0),Vector3(0.11,0.14,13.2),Color("3bd8fe"))
 for separator_z in [-6.25,-3.15,-0.05,3.08,6.25]:
  neon(stage,Vector3(0,0.15,separator_z),Vector3(8.0,0.05,0.12),Color("36bfff"))
 # Each bank retains three lane positions; unused lanes are neutral decorative
 # glass, not trapdoors or extra possible answers.
 for row in range(bridge_panels.size()):
  var options=bridge_panels[row]
  var count=options.size()
  var chosen_lanes=[0,1,2] if count==3 else ([0,2] if count==2 else [1])
  for index in range(count):
   var item:Dictionary=options[index]
   var new_position=Vector3((float(chosen_lanes[index])-1.0)*2.56,0.34,float(row_centers[row]))
   item["position"]=new_position
   item["mesh"].position=new_position
   item["body"].position=new_position
   item["label"].position=new_position+Vector3(0,0.14,0)
  for lane in range(3):
   if chosen_lanes.has(lane): continue
   var blank=box_mesh(stage,Vector3((float(lane)-1.0)*2.56,0.18,float(row_centers[row])),Vector3(2.33,0.08,2.42),Color("102743"))
   var inactive=StandardMaterial3D.new()
   inactive.albedo_color=Color(0.12,0.27,0.45,0.30)
   inactive.transparency=BaseMaterial3D.TRANSPARENCY_ALPHA
   inactive.roughness=0.34
   blank.material_override=inactive
'''

p.write_text(s)
print("Restored wide, full-width bridge deck while preserving the playable branching steps.")
