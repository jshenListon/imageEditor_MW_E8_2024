# constant.py

homepgIntroduction = """ Hi there! My name is Maximo Weber, and this is my Streamlit app. 
    Here, you can remove backgrounds from images, use a color picker, edit images, crop images, or explore the calculator on the next page.
    I have a passion for Sports, Music, Programming and enjoy building projects like this one.
    Feel free to navigate using the sidebar and explore what the app has to offer!"""

CANVAS_HTML = """
<!DOCTYPE html>
<html>
<head>
<style>
  .canvas-container {{
    position: relative;
  }}
  canvas {{
    border: 1px solid #d3d3d3;
  }}
  .button {{
    margin-top: 10px;
  }}
</style>
</head>
<body>
<div class="canvas-container">
  <canvas id="canvas" width="{canvas_width}" height="{canvas_height}"></canvas>
  <button class="button" id="downloadBtn">Download Edited Image</button>
</div>

<script>
  function drawOnCanvas() {{
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');

    // Draw the uploaded image on the canvas
    const img = new Image();
    img.src = 'data:image/png;base64,{img_base64}';
    img.onload = function() {{
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    }}

    // Initialize drawing state
    let drawing = false;
    let drawColor = '{draw_color}';
    let brushWidth = {brush_width};

    // Mouse events for drawing
    canvas.onmousedown = function(e) {{
      drawing = true;
      ctx.beginPath();
      ctx.moveTo(e.offsetX, e.offsetY);
    }};
    canvas.onmousemove = function(e) {{
      if (drawing) {{
        ctx.lineTo(e.offsetX, e.offsetY);
        ctx.strokeStyle = drawColor;
        ctx.lineWidth = brushWidth;
        ctx.stroke();
      }}
    }};
    canvas.onmouseup = function(e) {{
      drawing = false;
    }};

    // Download button functionality
    document.getElementById('downloadBtn').addEventListener('click', function() {{
      const dataURL = canvas.toDataURL('image/png');
      const link = document.createElement('a');
      link.href = dataURL;
      link.download = 'edited_image.png';
      link.click();
    }});
  }}

  // Run the drawing function on page load
  window.onload = drawOnCanvas;
</script>
</body>
</html>
"""
