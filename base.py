<html>
<head>
 <title>Flappy Bird</title>
 </head>
 <body>

<canvas id="myCanvas" width=320 height=480 style="background-color:powderblue">
</canvas>
  
<script> 

 var ctx = myCanvas.getContext("2d"); // Get the drawing context for the canvas
 var FPS = 40;                        // How many frames per second
 var jump_amount = -10;               // how much the bird jumps
 var max_fall_speed= +10;             // how fast the bird can fall
 var acceleration = 1;                // how quickly it goes from jumping to falling
 var pipe_speed = -2;                 // how quickly the pipes move left
 var game_mode = 'prestart';          // prestart, running or over
 var time_game_last_running;          // when did the game finish? 
 var pipes = [];                      // all our pipe-halves


 function MySprite (img_url) {
    this.x = 0;
    this.y = 0; 
    this.visible= true;
    this.velocity_x = 0;
    this.velocity_y = 0;
    this.MyImg = new Image();
    this.MyImg.src = img_url || '';
    this.angle = 0;                                  // How many degrees we are rotated
    this.flipV = false;                              // Are we flipped vertically 
    this.flipH = false;                              // Are we flipped horizontally
    }


 MySprite.prototype.Do_Frame_Things = function() {
    ctx.save();
    ctx.translate(this.x + this.MyImg.width/2, this.y + this.MyImg.height/2);
    ctx.rotate(this.angle * Math.PI / 180);                       // rotating
    if (this.flipV) ctx.scale(1,-1);                              // flipping
    if (this.flipH) ctx.scale(-1,1);
                    
    if (this.visible) ctx.drawImage(this.MyImg, -this.MyImg.width/2, -this.MyImg.height/2);
    this.x = this.x + this.velocity_x;
    this.y = this.y + this.velocity_y;                            // move the thing
    ctx.restore();                                                // unwarp the context
    }


 function ImagesTouching(thing1, thing2) {
     //
     // This function detects whether two MySprites are touching - very useful function
     // 
     if (!thing1.visible  || !thing2.visible) return false;         
     if (thing1.x >= thing2.x + thing2.MyImg.width || thing1.x + thing1.MyImg.width <= thing2.x) return false;   
     if (thing1.y >= thing2.y + thing2.MyImg.height || thing1.y + thing1.MyImg.height <= thing2.y) return false; 
     return true;                                                                                                
     }

function Got_Player_Input(MyEvent) {
   switch (game_mode) {
      case 'prestart': {
                        game_mode = 'running';
                        break;
                        } 
      case 'running': {
                        bird.velocity_y = jump_amount;
                        break;
                        } 
      case 'over': if (new Date() - time_game_last_running > 1000) {
                    reset_game();
                    game_mode = 'running';
                    break;
                    } 
       } // switch
   MyEvent.preventDefault();
   }

 addEventListener("touchstart", Got_Player_Input);     
 addEventListener("mousedown", Got_Player_Input);     
 addEventListener("keydown", Got_Player_Input);     

function make_bird_slow_and_fall() {
    if (bird.velocity_y < max_fall_speed) {
         bird.velocity_y = bird.velocity_y + acceleration;
         }  
    if (bird.y > myCanvas.height - bird.MyImg.height)  {      // gone off bottom
         bird.velocity_y = 0;
         game_mode = 'over';
         }
    }

function add_pipe(x_pos, top_of_gap, gap_width) {
    // First the top pipe
    var top_pipe = new MySprite();
    top_pipe.MyImg = pipe_piece;
    top_pipe.x = x_pos;
    top_pipe.y = top_of_gap - pipe_piece.height;
    top_pipe.velocity_x = pipe_speed;
    pipes.push(top_pipe);

    // Then the bottom pipe
    var bottom_pipe = new MySprite();
    bottom_pipe.MyImg = pipe_piece;
    bottom_pipe.flipV = true;
    bottom_pipe.x = x_pos;
    bottom_pipe.y = top_of_gap + gap_width;
    bottom_pipe.velocity_x = pipe_speed;
    pipes.push(bottom_pipe );
    }


function make_bird_tilt_appropriately() {
    if (bird.velocity_y < 0)  {
                 bird.angle= -15;                    // going up, point up
                 }
       else if (bird.angle < 70) {                   // max downward tilt is 70 degrees 
                 bird.angle = bird.angle + 4;        // going down, point more and more down
                 }
    }

function show_the_pipes() {
    for (var i=0; i < pipes.length; i++) {
             pipes[i].Do_Frame_Things(); 
             }
    }

function check_for_end_game() {
   for (var i=0; i < pipes.length; i++) 
     if (ImagesTouching(bird, pipes[i])) game_mode = "over";
   }

function display_intro_instructions () {
   ctx.font= "25px Arial";
   ctx.fillStyle= "red";
   ctx.textAlign="center";
   ctx.fillText("Press, touch or click to start", myCanvas.width / 2, myCanvas.height / 4);  
   }

function display_game_over () {
   var score = 0;
   for (var i=0; i < pipes.length; i++) 
        if (pipes[i].x < bird.x) score = score + 0.5;
   ctx.font= "30px Arial";
   ctx.fillStyle= "red";
   ctx.textAlign="center";
   ctx.fillText("Game Over", myCanvas.width / 2, 100);  
   ctx.fillText("Score: " + score, myCanvas.width / 2, 150);  
   ctx.font= "20px Arial";
   ctx.fillText("Click, touch, or press to play again", myCanvas.width / 2, 300);  
   }

function reset_game() {
      bird.y = myCanvas.height / 2;
      bird.angle= 0;
      pipes=[];
      add_all_my_pipes();
      }

function add_all_my_pipes() {
    add_pipe(500,  100, 140);
    add_pipe(800,   50, 140);
    add_pipe(1000, 250, 140);
    }

 var pipe_piece = new Image();
 pipe_piece.onload = add_all_my_pipes;
 pipe_piece.src = "https://s2js.com/img/etc/flappypipe.png" ;
 
 function Do_a_Frame () {
    ctx.clearRect(0, 0, myCanvas.width, myCanvas.height);   
    bird.Do_Frame_Things(); 

    switch (game_mode) {
        case 'prestart': {
                          display_intro_instructions();
                          break;
                          } 
        case 'running': {
                         time_game_last_running = new Date();  // Game was still running at this time
                         show_the_pipes();
                         make_bird_tilt_appropriately();
                         make_bird_slow_and_fall();
                         check_for_end_game();
                         break;
                         }
        case 'over': {
                      make_bird_slow_and_fall();
                      display_game_over();
                      break;
                      } 
        } // switch
    }
 
 var bird = new MySprite("https://s2js.com/img/etc/flappybird.png");
 bird.x = myCanvas.width / 3;
 bird.y = myCanvas.height / 2;

 setInterval(Do_a_Frame, 1000/FPS);                             // set my frame renderer
 </script>  
</body>
</html>