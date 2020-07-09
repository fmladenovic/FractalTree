function Leaf( center ) {
    this.center = center;


    this.jitter = function() {
        this.center.x += random( -0.5, 0.5 );
        this.center.y += random( -0.5, 0.5 );
    }

    this.show = function() {
        fill( 255, 0, 100, 100 );
        noStroke();
        ellipse( this.center.x, this.center.y, 8, 8);
    }
    
}