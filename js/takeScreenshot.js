
            html2canvas(arguments[0]).then(function(canvas) {
                var img = canvas.toDataURL("image/png");
                var link = document.createElement('a');
                link.download = 'screenshot.png';
                link.href = img;
                link.id='img_shot';
                link.click();
                return img;
            });

