import model
import view
import controller


if __name__ == '__main__':
    view = view.View()
    model = model.Model()
    controller = controller.Controller(view, model)
    controller.start()
    view.window.mainloop()