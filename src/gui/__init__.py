
def main():
    from twindow import TWindow
    from frame_date_difference import FrameDateDifference
    from frame_data_interval import FrameDateWithInterval
    from src import config_locale_app

    config_locale_app()
    
    window = TWindow(title="Date Calculator", themename="darkly")
    FrameDateDifference(window).pack(pady=10, padx=10, fill="both", expand=True)
    FrameDateWithInterval(window).pack(pady=10, padx=10, fill="both", expand=True)
    window.mainloop()

if __name__ == "__main__":
    main()