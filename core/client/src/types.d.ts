declare global {
  namespace model {
    interface User {
      id: number;
      name: string;
      email: string;
      image: string;
    }
    interface Filter {
      id: number;
      name: string;
      options: string[];
      icon: string;
    }
  }
  namespace request {
    interface Authorization {
      email: string;
      password: string;
    }
    interface Registration {
      name: string;
      email: string;
      password: string;
    }
    interface UserUpdating {
      name: string;
      email: string;
      image: string;
    }
    interface PasswordChanging {
      password: string;
      new_password: string;
    }
  }
  namespace response {
    interface Authorization {
      access: string;
      user: model.User;
    }
    interface Registration {
      name: string;
      email: string;
    }
  }
}

export {};
