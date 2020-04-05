<div class="cl-mcont">
    <div class='block'>
         <div class='header'>
             <h3>
                 TS-
             %if info.get('title',None):
               {{info['title']}}
             %end
             </h3>
         </div>
         <div class='content'>
            <div class="header">
                %if info.get("STATIC_ADMIN_PATH",None):
                    {{info["STATIC_ADMIN_PATH"]}}
                %end
            </div>
         </div>
    </div>
</div>
<script>

</script>