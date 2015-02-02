        <script>
            var names = 
            [
            "책 넘기는소리_sound of turning pages",
            "책 떨어지는 소리_sound of falling book",
            "의자 미는 소리_sound of dragging the chair",
            "발소리_sound of footsteps",
            "지우개로 지우는 소리_sound of rubbing out with an eraser on paper",
            "필통 여는 소리_sound of opening and closing the zipper of pencilcase",
            "샤프소리_sound of pen clicking",
            "문 여는 소리_sound of opening the door in the library",
            "문 닫는 소리_sound of closing the door in the library",
            "가방 여는 소리_sound of opening the zipper of the bag",
            "도서관의 조용한 곳에서 나는 소리_expressions on silence of liabrary",
            "복사기를 사용하는 소리_sound of copymachine",
            "계단을 올라가는 소리_sound of going up the stairs",
            "계단을 내려가는 소리_sound of going down the stairs",
            "종이를 구기는 소리_sound of crumpling paper",
            "종이를 자르는 소리_sound of cutting paper",
            "종이를 휴지통에 버리는 소리_sound of throwing the paper into the waste basket",
            "컴퓨터 키보드를 치는  소리_sound of typing on the keyboard",
            "컴퓨터 마우스를 움직이는 소리_sound of clicking mouse",
            "종이에 호치키스를 찍는 소리_sound of pressing staple"
            ]

            var i;
            var temp_span;
            var temp_p;
            var temp_temp_slash_div;
            var temp_button_div;
            var temp_button;

            for (i = 0; i < names.length; i++) {
                temp_span = document.createElement("span");
                temp_span.style.display= "block";
                temp_span.id = "span" + (i + 1);

                temp_p = document.createElement("p");
                temp_p.style.display = "inline";
                temp_p.id = "p" + (i + 1);
                temp_p.innerHTML = names[i];

                temp_slash_div = document.createElement("div");
                temp_slash_div.id = "divider";
                temp_slash_div.style.display = "inline";
                temp_slash_div.innerHTML = "/";

                temp_button_div = document.createElement("div");
                temp_button_div.id = "button_play";
                temp_button_div.style.display = "inline";

                temp_button = document.createElement("button");
                temp_button.type = "button";
                temp_button.id = "sori_" + (i + 1);
                temp_button.innerHTML = "PLAY";
             

                /*
                span    ->  p
                        ->  slash_div
                            slash_div   ->  button_div
                                            button_div  ->  button
                */

                temp_button_div.appendChild(temp_button);
                temp_slash_div.appendChild(temp_button_div);
                temp_span.appendChild(temp_slash_div);
                temp_span.appendChild(temp_p);
                
                document.getElementById("plist").appendChild(temp_span);

           }

        </script>


