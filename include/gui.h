#include <iostream>
// #include "Qt5" 

#include <wx/wx.h>

// include timekeeping 
#ifndef _WIN_32 
#include <time.h>
#else
#include <Windows.h>
#endif 

#define DEFAULT_MAX_TEXT_FIELD_CHAR 100
#define DEFAULT_TEXT_FIELD_LENGTH 30
#define TABOR_TEXT_CTRLS_LABEL_SEP 120
#define TABOR_TEXT_CTRLS_START_YPOS 100
#define TABOR_TEXT_CTRLS_YPOS_DELTA 20
#define TABOR_LABEL_X_OFFSET 60
#define TABOR_TITLE_OFFSET 40


#define TDC_LABELS_Y_OFFSET 420 // below start of tabor settings 


/* class Gui */
/* { */
/* public : */
/*     Gui(); */
/*     void read_text_field( TextField tf ) ; */

/* private : */
/*     TextField *create_text_field( int x1, int x2, int y1, int y2, int length, */
/* 				  int max_char, char *entry_ptr, char *default_text, */
/* 				  char *title, char *help_description ); */

/*     void read_text_field( TextField * tf) ; */
    
/*     void set_title( char *title ); */

/* } */



class MyApp : public wxApp
{
  public:
    virtual bool OnInit();
};




class Button : public wxFrame
{
public:
    Button(const wxString& title);

    void OnQuit(wxCommandEvent & event);
};



struct TaborTextCtrls
{
    wxTextCtrl *nsteps; //  1 or 2 = wminus only, 3 or 4 = wminus + wplus, 5 = everything

    wxTextCtrl *wminus;
    double wplus; // 130In //646445.9 135Te// 150Ce 1164702.5; // 1118649.8;// // //133Cs = 656250.0 //142Cs = 614447.6
// double wc = 657844.5; //130I648038.4 135Te // 150Ce 1166293.3; // 1120240.8;//1797579.0;// 1181999.3;// 1121410.2;// 130In = 672935.5; // 616040.4; // 657844.5;// 133Cs = 657844.5; //// 142Cs = 616040.4

    wxTextCtrl *wminus_phase;// -110.0;// 30.0;
    wxTextCtrl *wplus_phase;
    wxTextCtrl *wc_phase;

    wxTextCtrl *wminus_amp;// 0.0035;// 0.003;//0.0045;// 0.0075
    wxTextCtrl *wplus_amp;//0.22;  //0.11
    wxTextCtrl *wc_amp;
    
    wxTextCtrl *wminus_loops; // don't change
    wxTextCtrl *wplus_loops;// 133Cs = 100;
    wxTextCtrl *wc_loops;// 212;// 133Cs = 210
    
    wxTextCtrl * wminus_length;// 3 ; // 2
    wxTextCtrl *wplus_length;
    wxTextCtrl *wc_length; // don't change
    
    wxTextCtrl *tacc;// 220040;// 234075; // 60008 18500; // time in us
};



struct TDCDataGui
{
    wxStaticText *counts;
    wxStaticText *count_rate;
    wxStaticText *filtered_event_counts;
};







/* class TextCtrl : public wxTextCtrl */
/* { */
/* public : */
/*     TextEntry( const wxString & default_name ); */
/*     void OnEnter( wxCommandEvent &event ); */
/* }; */