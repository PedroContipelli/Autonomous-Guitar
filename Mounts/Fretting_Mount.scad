A = 31;
B = 23;
C = 26;
D = 12;
E = 32;
F = 15;
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
inf = 1000;
epsilon = 0.01;
//$fn = 50;

neck_length = 456;
neck_width1 = 43;
neck_height1 = 21;
neck_width2 = 58;
neck_height2 = 24;
// sound hole diameter: 100

string_spacing1 = 7;
string_spacing2 = 10;
string_radius = 0.375;
string_spread = 0.325;
string_height = 2;

fret_offsets = [36,70.5,103,133.5];
fret_width = 2;

QUARTER_INCH = 6.25;
EIGHTH_INCH = 3.125;

stick_length = EIGHTH_INCH+0.5;
stick_width = QUARTER_INCH;
stick_height = 115;

servo_x = 156;
servo_y = 65;
servo_z = 30;

stick_z = 19;

servo_vertical_spacing = 35;
servo_lateral_spacing = stick_length;

wall_thickness = QUARTER_INCH;

module_spacing = A+2*stick_length;

mount_width = servo_y+2*wall_thickness;

paperclip_radius = 1/2;
screw_radius = 1/2;

//modeling();
printing();
//print_sticks();

module modeling() {
    for (i = [0:3]) {
        panel(i);
        servo_set(i);
        sticks(i,0);
    }
    stick_guide();
    frets();
    strings();
    neck();
}

module printing() {
    projection()
    for (i = [0:3]) {
        translate([72,36,33.8])
        translate([i*(servo_y+3*wall_thickness),0,(3-i)*(module_spacing)])
        rotate([-90,90,0])
        panel(i);
    }
    
    projection(cut = true)
    translate([0,200,-22])
    stick_guide();
    
    projection()
    translate([0,285,0])
    stick_guide();
    
    projection()
    for (j = [0:1]) {
        for (i = [0:3]) {
            translate([154,230,0])
            translate([i*(neck_width2-13)+j*27,0,0])
            rotate([-90,0,0])
            sticks(i,50);
        }
    }
    
    projection(cut = true)
    for (i = [0:3]) {
        translate([222,95,23])
        translate([i*(D+3*string_spacing1+5),0,(3-i)*(module_spacing)])
        rotate([-90,90,0])
        panel(i);
    }
}

module print_sticks() {
    projection()
    for (j = [0:1]) {
        for (i = [0:3]) {
            translate([-30,-6,0])
            translate([i*(neck_width2-14)+j*23,0,0])
            rotate([-90,0,0])
            sticks(i,43);
        }
    }
}

module panel(i) {
    color("Gray")
    difference() {
        translate([-i*(module_spacing),0,0])
        union() {
            translate([
                servo_x-F,
                -wall_thickness,
                -neck_width2/2-wall_thickness])
            cube([
                wall_thickness,
                mount_width,
                neck_width2/2+servo_z+E+2*servo_vertical_spacing+4*wall_thickness]);
            
            translate([
                servo_x-F-2*servo_lateral_spacing,
                -D-3*string_spacing1+servo_y-2*string_spacing1+epsilon,
                servo_z+servo_vertical_spacing+E])
            cube([
                wall_thickness+2*servo_lateral_spacing,
                D+3*string_spacing1-2*epsilon,
                2*servo_vertical_spacing-E]);
        }
        
        translate([-i*(module_spacing),0,0])
        servo_set_holes();
        
        translate([-i*(module_spacing),0,0])
        string_cutout();
        
        neck();
        
        stick_guide_half();
        
        if (i%2==0) {
            translate([0,neck_width2/2,-50+4*string_height])
            cube([inf,inf,49.99]);
        } else {
            translate([0,-inf+neck_width2/2,-50+4*string_height])
            cube([inf,inf,49.99]);
        }
    }
}

module thin_panel(i) {
    color("Gray")
    translate([-i*(module_spacing),0,0])
    translate([
        servo_x-F,
        -wall_thickness+mount_width/2,
        -neck_width2/2-wall_thickness])
    cube([
        wall_thickness-1,
        mount_width/2,
        neck_width2/2+servo_z+E+2*servo_vertical_spacing+2*wall_thickness]);
}

module string_cutout() {
    translate([0,0,-epsilon])
    cube([neck_length,neck_width2,4*string_height]);
}

module stick_guide() {
    color("Gray")
    for (j = [0:1]) {
        translate([0,0,j*120])
        difference() {
            stick_guide_full();
            
            for (i = [0:3]) {
                thin_panel(i);
                if (j == 0) {
                    sticks(i,0);
                }
            }
        }
    }
}

module stick_guide_full() {
    color("Gray")
    translate([-epsilon,-wall_thickness,3*wall_thickness])
    cube([servo_x-F+wall_thickness+(module_spacing)/2,mount_width,wall_thickness]);
}

module stick_guide_half() {
    color("Gray")
    for (i = [0:1]) {
        translate([-epsilon,-wall_thickness,3*wall_thickness+i*120])
        cube([servo_x-F+wall_thickness+(module_spacing)/2,mount_width/2,wall_thickness-1]);
    }
}

module sticks(panel_index,stagger) {
    color("Gray")
    difference() {
        translate([-panel_index*module_spacing,0,0])
        // centered on middle of neck
        translate([servo_x-A,neck_width2/2-stick_width/2,servo_z])
        difference() {
            for (i = [0:1]) {
                for (j = [0:2]) {
                    spread_factor = 0.035; // spreads sticks to account for string spread
                    translate([
                        0,
                        -(i*3+j-2.5)*string_spacing1*(1+spread_factor*(3-panel_index)),
                        j*servo_vertical_spacing-stick_height+stick_z])
                    translate([-j*(servo_lateral_spacing+stagger),0,0])
                    stick();
                }
            }
        }
        
        // cut off bottoms of sticks
        translate([-100,-100,-inf])
        cube([inf,inf,inf+4*string_height]);
    }
}

module stick(thick) {
    difference() {
        cube([stick_length,stick_width,stick_height]);

        // notch for servo arm
        translate([0,0,stick_height-7])
        cube([O,stick_width,inf]);
    }
}



/* reference models */

module neck_cylinder() {
    scale([1,1,neck_height1/neck_width1*2])
    translate([0,neck_width2/2,0])
    rotate([0,90,0])
    cylinder(neck_length,neck_width1/2,neck_width2/2);
}

module neck() {
    color("#804000")
    difference() {
        neck_cylinder();
        
        translate([-epsilon,-epsilon,0])
        cube([inf,inf,neck_width2]);
    }
}

module strings() {
    for (i = [0:5]) {
        color("#bbbbbb")
        translate([0,neck_width2/2+(i-2.5)*string_spacing1,string_height])
        rotate([0,90,(i-2.5)*string_spread])
        cylinder(neck_length,string_radius,string_radius);
    }
}

module frets() {
    for (offset = fret_offsets) {
        intersection() {
            translate([offset,0,0])
            rotate([-90,0,0])
            cylinder(neck_width2,fret_width/2,fret_width/2);
            
            neck_cylinder();
        }
    }
}

module servo_set(i) {
    translate([-i*(module_spacing),0,0])
    translate([servo_x,servo_y,servo_z])
    for (i = [0:1]) {
        translate([0,-(i*3)*string_spacing1,0]) rotate([0,0,180]) servo();
        translate([0,-(i*3+1)*string_spacing1,servo_vertical_spacing]) rotate([0,0,180]) servo();
        translate([-2*servo_lateral_spacing,-(i*3+2)*string_spacing1,2*servo_vertical_spacing]) rotate([0,0,180]) servo();
    }
}

module servo_set_holes() {
    translate([servo_x,servo_y,servo_z])
    for (i = [0:1]) {
        for (j = [0:2]) {
            translate([0,-(i*3+j)*string_spacing1,j*servo_vertical_spacing])
            rotate([0,0,180]) translate([-inf,0,(E-B)/2-P]) cube([A+inf,D,B+P]);
        }
    }
}

module servo() {
    // body
    color("Blue") translate([0,0,(E-B)/2]) cube([I,D,B]);
    color("Blue") translate([F,0,0]) cube([J,D,E]);
    color("Blue") translate([I,D/2,(E-B)/2+D/2]) rotate([0,90,0]) cylinder(C-I, D/2, D/2);
    color("Blue") translate([I,D/2,E/2]) rotate([0,90,0]) cylinder(C-I,K/2,K/2);
    
    // wire
    color("Red") translate([0,(D-H)/2,(E-B)/2-P]) cube([G,H,P]);
    
    // arm
    color("White") translate([C,D/2,(E-B)/2+D/2]) rotate([0,90,0]) cylinder(A-C, L/2, L/2);
    for (i = [0:0.1:1]) {
        color("White") translate([A-O,D/2+i*N,(E-B)/2+D/2]) rotate([0,90,0]) cylinder(O,L/2*(1-i)+M/2*i,L/2*(1-i)+M/2*i);
    }
}