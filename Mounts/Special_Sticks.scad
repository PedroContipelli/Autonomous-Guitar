projection()
for (i = [0:3]) {
    translate([8.5*i + 3.625*1.5*(i%2),111*(i%2),0])
    rotate([0,0,180*i])
    special_stick();
}

module special_stick() {
    difference() {
        g = 8;
        union() {
            cube([3.625,111,6.25]);
            cube([7.25,g,6.25]);
        }
        h = 7;
        translate([0,111-7,0])
        cube([1.5,7,6.25]);
        
        cube([3.625,g/2,6.25]);
    }
}