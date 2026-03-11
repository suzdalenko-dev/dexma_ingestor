import os
import sys
import time
import servicemanager
import win32event
import win32service
import win32serviceutil

# Importa tu lógica actual
from main import run_once
from config import load_settings
from logger_setup import setup_logging


class ApiPollerService(win32serviceutil.ServiceFramework):
    _svc_name_ = "ApiPollerService"
    _svc_display_name_ = "Simple API Poller Suzdalenko"
    _svc_description_ = "Hace GET periódico a una API y guarda la respuesta en archivo."

    def __init__(self, args):
        super().__init__(args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.running = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.running = False
        win32event.SetEvent(self.stop_event)

    def SvcDoRun(self):
        servicemanager.LogInfoMsg(f"{self._svc_name_} - servicio arrancando")
        self.main()

    def main(self):
        setup_logging()
        settings = load_settings()

        while self.running:
            try:
                run_once(
                    url=settings.target_url,
                    output_dir=settings.output_dir,
                    timeout_seconds=settings.request_timeout_seconds,
                )
            except Exception as e:
                servicemanager.LogErrorMsg(f"{self._svc_name_} - error: {e}")
                time.sleep(10)

            # Espera hasta poll_interval o hasta que llegue orden de stop
            wait_result = win32event.WaitForSingleObject(
                self.stop_event,
                settings.poll_interval_seconds * 1000
            )

            if wait_result == win32event.WAIT_OBJECT_0:
                break


if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(ApiPollerService)

# python app\windows_service.py install
# python app\windows_service.py start
# python app\windows_service.py start
# python app\windows_service.py remove