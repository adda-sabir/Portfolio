figure(10)
clf
fig1=gcf;
set(fig1,'unit','centimeter','position',[1 1 25 18],'menubar','none','numberTitle','off','name','OptIdent : Laboratoire de Regulation - ECAM');
%set(fig1,'Position', [36.0 50.2 800 600]),

colorstring = 'w';
set(gcf,'color','w');

subplot(221)
plot(t,u),grid,title('MV (Puissance de chauffe) [%] ');xlabel('Temps [s]');ylabel('Action')
subplot(222);
plot(t,y),grid,title('PV (Temperature) [%]');xlabel('Temps [s]');ylabel('Sortie')

global Jfull xi

if isempty(xi)==1;
    K=-10;T1=100;T2=10;Tm=20;
    x0=[K,T1,T2,Tm];
    
else x0=xi;
end

x0=round(x0*100)/100;
x0(4)=abs(x0(4));

dx=2;dy=1;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
c10=uicontrol('Visible','on','Style','text','unit','centimeter','position',[1+dx 5.2+dy 4 1.5],'string','Coefficients :','BackgroundColor',colorstring,'FontSize',12);
c10=uicontrol('Visible','on','Style','text','unit','centimeter','position',[1+dx 5+dy 4 1.2],'string','________________________','BackgroundColor',colorstring,'FontSize',2);
c11=uicontrol('Visible','on','Style','text','unit','centimeter','position',[1.5+dx 4.2+dy 1 1.5],'string','Kp :','BackgroundColor',colorstring,'FontSize',12);
c12=uicontrol('Visible','on','Style','text','unit','centimeter','position',[1.5+dx 3.2+dy 1 1.5],'string','T1 :','BackgroundColor',colorstring,'FontSize',12);
c13=uicontrol('Visible','on','Style','text','unit','centimeter','position',[1.5+dx 2.2+dy 1 1.5],'string','T2 :','BackgroundColor',colorstring,'FontSize',12);
c14=uicontrol('Visible','on','Style','text','unit','centimeter','position',[1.5+dx 1.2+dy 1 1.5],'string','Tm :','BackgroundColor',colorstring,'FontSize',12);

c21=uicontrol('Visible','on','Style','edit','unit','centimeter','position',[2.5+dx 4.2+dy 2 1.5],'BackgroundColor',colorstring,'FontSize',12,'Callback','Kp0=get(c21,''string'');x0(1)=str2num(Kp0);');
c22=uicontrol('Visible','on','Style','edit','unit','centimeter','position',[2.5+dx 3.2+dy 2 1.5],'BackgroundColor',colorstring,'FontSize',12,'Callback','T10=get(c22,''string'');x0(2)=str2num(T10);');
c23=uicontrol('Visible','on','Style','edit','unit','centimeter','position',[2.5+dx 2.2+dy 2 1.5],'BackgroundColor',colorstring,'FontSize',12,'Callback','T20=get(c23,''string'');x0(3)=str2num(T20);');
c24=uicontrol('Visible','on','Style','edit','unit','centimeter','position',[2.5+dx 1.2+dy 2 1.5],'BackgroundColor',colorstring,'FontSize',12,'Callback','Tm0=get(c24,''string'');x0(4)=str2num(Tm0);');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

dec=10;dx=3;
c301=uicontrol('Visible','on','Style','text','unit','centimeter','position',[1+dx+dec 5.2+dy 4 1.5],'string','Mise à l''échelle :','BackgroundColor',colorstring,'FontSize',12);
c30=uicontrol('Visible','on','Style','text','unit','centimeter','position',[1+dx+dec 5+dy 4 1.2],'string','________________________','BackgroundColor',colorstring,'FontSize',2);
c31=uicontrol('Visible','on','Style','text','unit','centimeter','position',[1.5+dx+dec 4.2+dy 3 1.5],'string','Y_initial :','BackgroundColor',colorstring,'FontSize',12);
c32=uicontrol('Visible','on','Style','text','unit','centimeter','position',[1.5+dx+dec 3.2+dy 3 1.5],'string','Delta U :','BackgroundColor',colorstring,'FontSize',12);
c33=uicontrol('Visible','on','Style','text','unit','centimeter','position',[1.5+dx+dec 2.2+dy 3 1.5],'string','T_step :','BackgroundColor',colorstring,'FontSize',12);

dx=5;
c41=uicontrol('Visible','on','Style','edit','unit','centimeter','position',[2.5+dx+dec 4.2+dy 2 1.5],'BackgroundColor',colorstring,'FontSize',12,'Callback','y0=get(c41,''string'');y0=str2num(y0);');
c42=uicontrol('Visible','on','Style','edit','unit','centimeter','position',[2.5+dx+dec 3.2+dy 2 1.5],'BackgroundColor',colorstring,'FontSize',12,'Callback','du=get(c42,''string'');du=str2num(du);');
c43=uicontrol('Visible','on','Style','edit','unit','centimeter','position',[2.5+dx+dec 2.2+dy 2 1.5],'BackgroundColor',colorstring,'FontSize',12,'Callback','tstep=get(c43,''string'');tstep=str2num(tstep);');

set(c21,'string',num2str(x0(1)));
set(c22,'string',num2str(x0(2)));
set(c23,'string',num2str(x0(3)));
set(c24,'string',num2str(x0(4)));

set(c41,'string',num2str(y0));
set(c42,'string',num2str(du));
set(c43,'string',num2str(tstep));

c44=uicontrol('Visible','on','Style','pushbutton','unit','centimeter','position',[2.5+dx+dec 0.2+dy 2 1.5],'BackgroundColor',colorstring,'FontSize',12,'String','Start','Callback',...
'set(c301,''visible'',''off'');set(c30,''visible'',''off'');set(c31,''visible'',''off'');set(c32,''visible'',''off'');set(c33,''visible'',''off'');set(c41,''visible'',''off'');set(c42,''visible'',''off'');set(c43,''visible'',''off'');set(c44,''visible'',''off'');Yid=y-y0;Yid=Yid/du;Yid=Yid(tstep:end);Tid=t(tstep:end);Tid=Tid-Tid(1); Jfull=[];a=optimset(''MaxIter'',200,''MaxFunEvals'',200);[x]=fminsearch(''idregtemppidvdg'',x0,a,Tid,Yid,u(tstep:end)/du);subplot(211);title(''End optimisation '');xlabel(''Temps [s]'');xi=x;set(fig1,''menubar'',''figure'')');