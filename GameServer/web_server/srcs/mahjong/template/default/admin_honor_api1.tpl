<script type="text/javascript" src="{{info['STATIC_ADMIN_PATH']}}/js/agent_create.js"></script>
<style type="text/css">
    .config-table td{text-align:center;font-size:13px;vertical-align:middle}
</style>
<div class="cl-mcont">
    <div class='block'>
         <div class='header'>
             <h3>
             %if info.get('title',None):
               {{info['title']}}
             %end
           </h3>
         </div>
    </div>
    <table class='table config-table' style='margin:0 20%;width:60%'>
        <tr>
          <td align='center'>接口描述</td>
        </tr>
        <tr>
          <td align='center'>
              <a href='http://127.0.0.1:9798/api/honor.html'>荣誉场接口</a>
          </td>
        </tr>
    </table>
</div>

%rebase admin_frame_base