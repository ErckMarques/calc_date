
def main():
    from twindow import TWindow
    from frame_date_difference import FrameDateDifference
    from frame_data_interval import FrameDateWithInterval
    from config import config_locale_app

    config_locale_app()
    
    window = TWindow()
    FrameDateDifference(window).pack(fill="both", expand=True)
    FrameDateWithInterval(window).pack(fill="both", expand=True)
    window.mainloop()

if __name__ == "__main__":
    main()