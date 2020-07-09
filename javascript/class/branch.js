function Branch( begin, end ) {
    this.begin = begin;
    this.end = end;
    this.finished = false;

    this.jitter = function() {
        this.end.x += random( -1, 1 );
        this.end.y += random( -1, 1 );

    }
    this.show = function() {
        stroke(255);
        line( this.begin.x, this.begin.y, this.end.x, this.end.y );
    }
    this.branch = function() {
        this.finished = true;
        var arrToRet = [];
        var dir = p5.Vector.sub( this.end, this.begin );
        dir.mult( 0.67 );
        dir.rotate( PI / 6 );
        var newEnd = p5.Vector.add( this.end, dir );
        var right = new Branch(this.end, newEnd);
        dir.rotate( -PI / 2 );
        var newEnd = p5.Vector.add( this.end, dir );
        var left = new Branch(this.end, newEnd);
        arrToRet[0] = left;
        arrToRet[1] = right;
        return arrToRet;
    }

}