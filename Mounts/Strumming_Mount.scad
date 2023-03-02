A = 31; // height
B = 23; // main body length
C = 26; // height before arm
D = 12; // width
E = 32; // full length
F = 15; // height until mounting points
G = 5; // from bottom of servo to top of wires
H = 4; // width of wires
I = 22; // height of body
J = 2; // thickness of wings
K = 5; // width of axel bump
L = 7; // major diameter of arm
M = 4; // minor diameter of arm
N = 14.5; // arm length
O = 1.5; // arm thickness
P = H/3; // width of wire
servo_box_across = D * 4.5;
mount_height = 15; // Needs to be measured exactly
mount_thickness = 20;
mount_across = 130;
mount_cut_across = 112;
inf = 200;
epsilon = 0.01;
$fn = 50;

sound_hole_diameter = 100;
string_height = 14;
string_spacing = 50/5;
string_diameter = 1.5;
string_clearance = 4;

wall_thickness = 4.5;

flange_length = 20;

modeling();
//printing();

module printing() {
    for (i = [0:1]) {
        translate([i*(B+3*wall_thickness),0,(A-F)+wall_thickness])
        rotate([0,-90,0])
        difference() {
            mount();
            
            translate([inf/2,0,0])
            cube([inf,inf,inf],center=true);
        }
    }
}

module modeling() {
    guitar();
    color("Gray")
    mount();
    
    many() servo();
}

module many() {
    for (j = [0:1]) {
        rotate([0,0,j*180])
        for (i = [0:2]) {
            translate([-A,(i-0.75)*2*string_spacing-D/2,string_height+string_clearance+wall_thickness-(E-B)/2])
            children(0);
        }
    }
}

module mount() {
    difference() {
    translate([0,0,string_height+B/2+wall_thickness+string_clearance])
    difference() {
        union() {
            cube([2*(A-F)+2*wall_thickness,5*string_spacing+D+2*wall_thickness,B+2*wall_thickness],center=true);
            
            translate([0,0,-(string_height+string_clearance+wall_thickness+B)/2])
            cube([2*(A-F)+2*wall_thickness,sound_hole_diameter,string_height+string_clearance+wall_thickness],center=true);
            
            translate([0,0,-(string_height+string_clearance)-(wall_thickness+B)/2])
                cube([2*(A-F)+2*wall_thickness,sound_hole_diameter+2*flange_length,wall_thickness],center=true);
        }
        
        //cube([inf,5*string_spacing+D,B],center=true);
        
        cube([2*(A-F),5*string_spacing+D,inf],center=true);
    }
        translate([0,0,(string_height+string_clearance)/2-epsilon])
        cube([inf,sound_hole_diameter-2*wall_thickness,string_height+string_clearance],center=true);
    
        many() servo_hole();
    }
}

module guitar() {
    color("#804000")
    difference() {
        translate([0,0,-1])
        cube([1.5*sound_hole_diameter, 1.5*sound_hole_diameter, 1], center=true);
        
        cylinder(20, sound_hole_diameter/2, sound_hole_diameter/2, center=true);
    }
    
    for (i = [0:5]) {
        translate([-0.75*sound_hole_diameter,(i-2.5)*string_spacing,string_height])
        rotate([0,90,0])
        cylinder(1.5*sound_hole_diameter, string_diameter/2, string_diameter/2);
    }
}

module servo() {
    // body
    color("Blue") translate([0, 0, (E-B)/2]) cube([I, D, B]);
    color("Blue") translate([F, 0, 0]) cube([J, D, E]);
    color("Blue") translate([I, D/2, (E-B)/2+D/2])
        rotate([0, 90, 0]) cylinder(C-I, D/2, D/2);
    color("Blue") translate([I, D/2, E/2])
        rotate([0, 90, 0]) cylinder(C-I, K/2, K/2);
    
    // wire
    color("Red") translate([0, (D-H)/2, (E-B)/2-P]) cube([G, H, P]);
    
    // arm
    color("White") translate([C, D/2, (E-B)/2+D/2])
        rotate([0, 90, 0]) cylinder(A-C, L/2, L/2);
    for (i = [0:0.01:1]) {
        color("White") translate([A-O, D/2, (E-B)/2+D/2-i*N])
            rotate([0, 90, 0]) cylinder(O, L/2*(1-i) + M/2*i,
                                           L/2*(1-i) + M/2*i);
    }
}

module servo_hole() {
    translate([0, 0, (E-B)/2-P]) cube([I, D, B+P]);
}
