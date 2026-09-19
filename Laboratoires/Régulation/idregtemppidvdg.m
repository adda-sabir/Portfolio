function J=id(x,t,y,u)

x
global Jfull c11 c12 c13 c14 c21 c22 c23 c24
%x(3)=0
H=tf(x(1),conv([x(2) 1],[x(3) 1]));
set(H,'InputDelay',abs(x(4)));

yst=step(H,t);
yst=y(1)+yst*(u(end)-u(1));

J=sqrt((y-yst)'*(y-yst))/length(y);
[Emax,indEmax]=max((y-yst).^2);

f1=gcf;
set(f1,'unit','centimeter','Position', [1 1 22 15]),
subplot(211)

colorstring = 'w';
set(gcf,'color','w');

plot(t,y,t,yst,'k',[t(indEmax),t(indEmax)],[y(indEmax),yst(indEmax)],'r.',[t(indEmax),t(indEmax)],[y(indEmax),yst(indEmax)],'r');title('Optimizing...');xlabel('Temps [s]');grid


Jfull=[Jfull J];
x=round(x*100)/100;x(4)=abs(x(4));dx=2;dy=1;
if length(Jfull)==1,
c10=uicontrol('Visible','on','Style','text','unit','centimeter','position',[1+dx 5.2+dy 4 1.5],'string','Coefficients du modèle :','BackgroundColor',colorstring,'FontSize',12);
c10=uicontrol('Visible','on','Style','text','unit','centimeter','position',[1+dx 5+dy 4 1.2],'string','________________________','BackgroundColor',colorstring,'FontSize',2);
c11=uicontrol('Visible','on','Style','text','unit','centimeter','position',[1.5+dx 4.2+dy 1 1.5],'string','Kp :','BackgroundColor',colorstring,'FontSize',12);
c12=uicontrol('Visible','on','Style','text','unit','centimeter','position',[1.5+dx 3.2+dy 1 1.5],'string','T1 :','BackgroundColor',colorstring,'FontSize',12);
c13=uicontrol('Visible','on','Style','text','unit','centimeter','position',[1.5+dx 2.2+dy 1 1.5],'string','T2 :','BackgroundColor',colorstring,'FontSize',12);
c14=uicontrol('Visible','on','Style','text','unit','centimeter','position',[1.5+dx 1.2+dy 1 1.5],'string','Tm :','BackgroundColor',colorstring,'FontSize',12);

c21=uicontrol('Visible','on','Style','text','unit','centimeter','position',[2.5+dx 4.2+dy 2 1.5],'string',x(1),'BackgroundColor',colorstring,'FontSize',12);
c22=uicontrol('Visible','on','Style','text','unit','centimeter','position',[2.5+dx 3.2+dy 2 1.5],'string',x(2),'BackgroundColor',colorstring,'FontSize',12);
c23=uicontrol('Visible','on','Style','text','unit','centimeter','position',[2.5+dx 2.2+dy 2 1.5],'string',x(3),'BackgroundColor',colorstring,'FontSize',12);
c24=uicontrol('Visible','on','Style','text','unit','centimeter','position',[2.5+dx 1.2+dy 2 1.5],'string',x(4),'BackgroundColor',colorstring,'FontSize',12);
else
   set(c21,'string',x(1))   
   set(c22,'string',max(x(2),x(3)))   
   set(c23,'string',min(x(2),x(3)))   
   set(c24,'string',x(4))   
end



subplot(235)
plot(Jfull);title('Fonction de coût');grid

subplot(236)
semilogy(Jfull);title('Fonction de coût');grid
drawnow