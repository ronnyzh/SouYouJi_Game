function getSelectServerSwitchState(){ return false; }

function getShowOtherWallet(){ return true; }

function getLanguage(){ return 'en'; }

function isPublicLock(gid)
{
	switch(gid)
	{
		//case 'game565':
		case 'game548':
		//case 'game549':
		case 'game570':
			return true;

		default:
			return false;
	}
}

function isPublicVersion(){ return false; }

function isPrintURL(){ return true; }

function isPrintProtoCmd(){ return true;}

function isTestSpeed(){ return false; }

function getTSConfigs()
{
    return ['1000','445','1'];
}

function getResRoot()
{
	//return 'http://123.207.238.38:8098/xin/g365/publish_source/res/';
	return 'res/';
}

function getTextResRoot()
{
	return 'res/';
}

function getLoginType()
{
	return 3;
}

function isHotGame(game)
{
	switch(game)
	{
		case 'game449':
		case 'game555':
		case 'game556':
			return true;
		default:
			return false;
	}
}

function AllFundVisible()
{
	return true;
}

function getGameSubPageType(gameid)
{
	switch(gameid)
	{
		case 549:
			return 1;
		default:
			return 0;
	}
}

/////////////////////////////////////////////////////////

function getQueryString(name)
{
	var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
	var r = window.location.search.substr(1).match(reg);
	if(r!=null)return  unescape(r[2]); return null;
}

function callJsOpenWindow(target_url)
{
	if(window != top)
		top.location.href = target_url;
	else
		window.location.href = target_url;
}