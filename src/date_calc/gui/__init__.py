
def main():
    from date_calc.gui.twindow import TWindow
    from date_calc.gui.frame_date_difference import FrameDateDifference
    from date_calc.gui.frame_data_interval import FrameDateWithInterval
    from date_calc import config_locale_app

    config_locale_app()
    
    window = TWindow(title="Date Calculator", themename="darkly")
    FrameDateDifference(window).pack(pady=10, padx=10, fill="both", expand=True)
    FrameDateWithInterval(window).pack(pady=10, padx=10, fill="both", expand=True)
    window.mainloop()

if __name__ == "__main__":
    main()